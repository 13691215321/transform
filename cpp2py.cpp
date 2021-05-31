#include "stdafx.h"
#include "CallPython.h"

CCallPython* CCallPython::m_spCCallPython = new CCallPython;

CCallPython::CCallPython()
{
}


CCallPython::~CCallPython()
{
    // 关闭Python解释器
    Py_Finalize();
}

//获取单例对象
CCallPython* CCallPython::GetInstance()
{
    //if (m_spHIKAGVComm == NULL)
    //{
    //    m_spHIKAGVComm = new CHIKAGVComm;
    //}
    return m_spCCallPython;
}

//销毁对象
void CCallPython::Destory()
{
    if (m_spCCallPython != NULL)
    {
        delete m_spCCallPython;
        m_spCCallPython = NULL;
    }
}

bool CCallPython::Init(char * pchPyfile)
{
    Py_Initialize();
    PyRun_SimpleString("import sys");
    PyRun_SimpleString("sys.path.append('./Plugins')");
    // 打开.py文件。注意参数是"Add"而不是"Add.py"
    m_pModule = PyImport_ImportModule(pchPyfile);

    return true;
}

bool CCallPython::CallInit()
{
    // 读取文件中的函数，参数为函数名
    PyObject* pFunc = PyObject_GetAttrString(m_pModule, "init");
    if (!pFunc)
    {
        return false;
    }
    PyObject* args = PyTuple_New(2);
    import_array();
    // 构建参数，包含两个int
    PyObject* arg0 = Py_BuildValue("s", "D:\\goertek\\roadnet.json"); // 字符串
    //id, x, y, status, online, speed, goal_x, goal_y
    double CArrays[2][8] = { { 1, 1.3, 2.4, 1, 0, 5.6 ,0,0 },{ 2,4.5, 7.8, 1, 0, 8.9 ,0,0 } }; //定义一个2 X 8的数组
    npy_intp Dims[2] = { 2, 8 }; //给定维度信息
    // 第一个参数2表示维度，第二个为维度数组Dims,第三个参数指出数组的类型，第四个参数为数组
    PyObject *PyArray = PyArray_SimpleNewFromData(2, Dims, NPY_DOUBLE, CArrays);

    PyTuple_SetItem(args, 0, arg0);
    PyTuple_SetItem(args, 1, PyArray);

    // 调用函数得到返回值
    PyObject* res = PyObject_CallObject(pFunc, args);
    if (!res)
    {
        // 打印错误信息
        PyErr_Print();
    }
    else
    {
        // 从PyObject中得到返回值
        int output = PyFloat_AsDouble(res);
   }
    return true;
}

bool CCallPython::Callsetgoal(int iAGVId)
{
    // 读取文件中的函数，参数为函数名
    PyObject* pFunc = PyObject_GetAttrString(m_pModule, "set_goal");
    if (!pFunc)
    {
        return false;
    }

    //agv_id,stationcode,x,y,goal_x,goal_y
    int stationcode = 0;
    double x=0.0, y = 0.0, goal_x = 0.0, goal_y = 0.0;

    // 构建参数，包含两个int
    PyObject* args = Py_BuildValue("iidddd", iAGVId, stationcode, x,y, goal_x, goal_y);

    // 调用函数得到返回值
    PyObject* res = PyObject_CallObject(pFunc, args);
    if (!res)
    {
        // 打印错误信息
        PyErr_Print();
    }
    else
    {
        // 从PyObject中得到返回值
        int output = PyFloat_AsDouble(res);
    }
    return true;
}

bool CCallPython::Callupdate()
{
    // 读取文件中的函数，参数为函数名
    PyObject* pFunc = PyObject_GetAttrString(m_pModule, "update");
    if (!pFunc)
    {
        return false;
    }
    PyObject* args = PyTuple_New(1);
    import_array();
    double CArrays[2][8] = { { 1, 1.3, 2.4, 1, 0, 5.6 ,0,0 },{ 2,4.5, 7.8, 1, 0, 8.9 ,0,0 } }; //定义一个2 X 8的数组
    npy_intp Dims[2] = { 2, 8 }; //给定维度信息
    // 第一个参数2表示维度，第二个为维度数组Dims,第三个参数指出数组的类型，第四个参数为数组
    PyObject *PyArray = PyArray_SimpleNewFromData(2, Dims, NPY_DOUBLE, CArrays);

    PyTuple_SetItem(args, 0, PyArray);

    // 调用函数得到返回值
    PyObject* res = PyObject_CallObject(pFunc, args);
    if (!res)
    {
        // 打印错误信息
        PyErr_Print();
    }
    else
    {
        // 从PyObject中得到返回值
        int output = PyFloat_AsDouble(res);
    }
    return true;
}
