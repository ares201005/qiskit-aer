/* Created by CMake. DO NOT EDIT; changes will be lost. */
#ifndef _MODULES_H
#define _MODULES_H

#include <Python.h>

#ifdef __cplusplus
extern "C" {
#endif /* __cplusplus */

#if PY_MAJOR_VERSION < 3
#else /* PY_MAJOR_VERSION >= 3*/
#endif /* PY_MAJOR_VERSION >= 3*/

#ifdef __cplusplus
}
#endif /* __cplusplus */

void modules_LoadAllPythonModules(void)
{
}

#ifndef EXCLUDE_LOAD_ALL_FUNCTION
void CMakeLoadAllPythonModules(void)
{
  modules_LoadAllPythonModules();
}
#endif /* !EXCLUDE_LOAD_ALL_FUNCTION */

#ifndef EXCLUDE_PY_INIT_WRAPPER
static void Py_Initialize_Wrapper()
{
  modules_LoadAllPythonModules();
  Py_Initialize();
}
#define Py_Initialize Py_Initialize_Wrapper
#endif /* !EXCLUDE_PY_INIT_WRAPPER */

#endif /* !_MODULES_H */
