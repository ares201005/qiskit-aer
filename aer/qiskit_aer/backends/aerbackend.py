# -*- coding: utf-8 -*-

# Copyright 2018, IBM.
#
# This source code is licensed under the Apache License, Version 2.0 found in
# the LICENSE.txt file in the root directory of this source tree.

"""
Qiskit Aer qasm simulator backend.
"""

import json
import logging
import datetime
import uuid
import numpy as np

import qiskit
from qiskit.backends import BaseBackend
from qiskit.qobj import qobj_to_dict
from qiskit.result._result import Result
from .aerjob import AerJob
from .aersimulatorerror import AerSimulatorError
from ..noise import NoiseModel

# Logger
logger = logging.getLogger(__name__)


class AerJSONEncoder(json.JSONEncoder):
    """
    JSON encoder for NumPy arrays and complex numbers.

    This functions as the standard JSON Encoder but adds support
    for encoding:
        complex numbers z as lists [z.real, z.imag]
        ndarrays as nested lists.
    """

    # pylint: disable=method-hidden,arguments-differ
    def default(self, obj):
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        if isinstance(obj, complex):
            return [obj.real, obj.imag]
        return super().default(obj)


class AerJSONDecoder(json.JSONDecoder):
    """
    JSON decoder for complex expectation value snapshots.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(object_hook=self.object_hook, *args, **kwargs)

    def decode_complex(self, obj):
        if isinstance(obj, list) and len(obj) == 2:
            if obj[1] == 0.:
                obj = obj[0]
            else:
                obj = obj[0] + 1j * obj[1]
        return obj

    # pylint: disable=method-hidden
    def object_hook(self, obj):
        """Special decoding rules for simulator output."""

        # Decode snapshots
        if 'snapshots' in obj:
            # Decode observables
            if 'observables' in obj['snapshots']:
                for key in obj['snapshots']['observables']:
                    for j, val in enumerate(obj['snapshots']['observables'][key]):
                        obj['snapshots']['observables'][key][j]['value'] = self.decode_complex(val['value'])
        return obj


class AerBackend(BaseBackend):
    """Qiskit Aer Backend class."""

    def __init__(self, configuration, simulator_wrapper, provider=None,
                 json_decoder=AerJSONDecoder):
        """Aer class for backends.

        This method should initialize the module and its configuration, and
        raise an exception if a component of the module is
        not available.

        Args:
            configuration (dict): configuration dictionary
            provider (BaseProvider): provider responsible for this backend
            simulator_wrapper (class): Aer simulator wrapper cython class
            provider (BaseProvider): provider responsible for this backend
            json_decoder (JSONDecoder): JSON decoder for simulator output

        Raises:
            FileNotFoundError if backend executable is not available.
            QISKitError: if there is no name in the configuration
        """
        super().__init__(configuration, provider=provider)
        # Extract the default basis gates set from backend configuration
        self._default_basis_gates = configuration.get('basis_gates')
        self._noise_model = None
        self._simulator = simulator_wrapper
        self._json_decoder = json_decoder

    def reset(self):
        """Reset the Aer Backend.

        This clears any set noise model or config.
        """
        self.clear_config()
        self.clear_noise_model()

    def run(self, qobj):
        """Run a qobj on the backend."""
        job_id = str(uuid.uuid4())
        aer_job = AerJob(self, job_id, self._run_job, qobj)
        aer_job.submit()
        return aer_job

    def _run_job(self, job_id, qobj):
        self._validate(qobj)
        qobj_str = json.dumps(qobj_to_dict(qobj), cls=AerJSONEncoder)
        output = json.loads(self._simulator.execute(qobj_str),
                            cls=self._json_decoder)
        # Check results
        # TODO: Once https://github.com/Qiskit/qiskit-terra/issues/1023
        #       is merged this should be updated to deal with errors using
        #       the Result object methods
        if not output.get("success", False):
            logger.error("AerBackend: simulation failed")
            raise AerSimulatorError(output.get("status", None))
        # Add result metadata
        output["job_id"] = job_id
        output["date"] = datetime.datetime.today().strftime('%Y-%m-%d %H:%M:%S')
        output["backend_name"] = self.DEFAULT_CONFIGURATION['name']
        output["backend_version"] = "0.0.1"  # TODO: get this from somewhere else
        # Parse result dict into Result class
        exp_results = output.get("results", {})
        experiment_names = [data.get("header", {}).get("name", None)
                            for data in exp_results]
        qobj_result = qiskit.qobj.Result(**output)
        qobj_result.results = [qiskit.qobj.ExperimentResult(**res) for res in exp_results]
        return Result(qobj_result, experiment_names=experiment_names)

    def set_noise_model(self, noise_model=None):
        """Set a simulation noise model for the backend."""
        if noise_model is None:
            # If None clear current noise model
            self.clear_noise_model()
            return

        # Attach noise model to backend
        if isinstance(noise_model, NoiseModel):
            self._noise_model = noise_model
            # Convert to dict for json serialization
            noise_model_dict = noise_model.as_dict()
        elif isinstance(noise_model, dict):
            noise_model_dict = noise_model
            # Convert to NoiseModel object to attach
            self._noise_model = NoiseModel()
            self._noise_model.from_dict(noise_model)
        else:
            raise AerSimulatorError("Invalid Qiskit Aer noise model.")

        # Attach noise model to wrapper
        self._simulator.set_noise_model(json.dumps(noise_model_dict, cls=AerJSONEncoder))
        # Update basis gates to use the gates in the noise model
        basis_gates = noise_model_dict.get("basis_gates", None)
        if isinstance(basis_gates, str):
            self._configuration["basis_gates"] = basis_gates

    def get_noise_model(self):
        """Return the current backend noise model."""
        return self._noise_model

    def clear_noise_model(self):
        """Reset simulator to ideal (no noise)."""
        self._noise_model = None
        self._simulator.clear_noise_model()
        # Reset to default basis gates
        self._configuration["basis_gates"] = self._default_basis_gates

    def set_config(self, config=None):
        """Set config of simulator backend."""
        if config is None:
            self.clear_config()
        else:
            self._simulator.set_config(json.dumps(config, cls=AerJSONEncoder))

    def clear_config(self):
        """Clear config of simulator backend."""
        self._simulator.clear_config()

    def set_max_threads_shot(self, threads):
        """
        Set the maximum threads used for parallel shot execution.

        Args:
            threads (int): the thread limit, set to -1 to use maximum available

        Note that using parallel shot evaluation disables parallel circuit
        evaluation.
        """
        self._simulator.set_max_threads_shot(int(threads))

    def set_max_threads_circuit(self, threads):
        """
        Set the maximum threads used for parallel circuit execution.

        Args:
            threads (int): the thread limit, set to -1 to use maximum available

        Note that using parallel circuit evaluation disables parallel shot
        evaluation.
        """
        self._simulator.set_max_threads_circuit(int(threads))

    def set_max_threads_state(self, threads):
        """
        Set the maximum threads used for state update parallel  routines.

        Args:
            threads (int): the thread limit, set to -1 to use maximum available.

        Note that using parallel circuit or shot execution takes precidence over
        parallel state evaluation.
        """
        self._simulator.set_max_threads_state(int(threads))

    def _validate(self, qobj):
        # TODO
        return

    def __repr__(self):
        """Official string representation of an AerBackend."""
        display = "{}('{}')".format(self.__class__.__name__, self.name())
        if self.provider is not None:
            display = display + " from {}()".format(self.provider)
        if self._noise_model is not None:
            display = display + " with {}".format(self._noise_model)
        return "<" + display + ">"