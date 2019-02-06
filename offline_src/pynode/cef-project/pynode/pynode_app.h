// Copyright (c) 2017 Alex Socha
// https://alexsocha.github.io/pynode

#ifndef CEF_PYNODE_PYNODE_APP_H_
#define CEF_PYNODE_PYNODE_APP_H_

#include "include/cef_app.h"

class PyNodeApp : public CefApp,
public CefBrowserProcessHandler {
public:
    PyNodeApp();
    static bool RecieveJavaScript(std::string message);
    virtual CefRefPtr<CefBrowserProcessHandler> GetBrowserProcessHandler() OVERRIDE { return this; }

virtual void OnContextInitialized() OVERRIDE;

private:
IMPLEMENT_REFCOUNTING(PyNodeApp);
};

#endif
