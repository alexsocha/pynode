// Copyright (c) 2017 Alex Socha
// http://www.alexsocha.com/pynode

#include "pynode_app.h"
#include <X11/Xlib.h>
#include "include/base/cef_logging.h"

namespace {
int XErrorHandlerImpl(Display *display, XErrorEvent *event) {
  LOG(WARNING)
        << "X error received: "
        << "type " << event->type << ", "
        << "serial " << event->serial << ", "
        << "error_code " << static_cast<int>(event->error_code) << ", "
        << "request_code " << static_cast<int>(event->request_code) << ", "
        << "minor_code " << static_cast<int>(event->minor_code);
  return 0;
}

int XIOErrorHandlerImpl(Display *display) {
  return 0;
}
}

int main(int argc, char* argv[]) {
  CefMainArgs main_args(argc, argv);
  
  int exit_code = CefExecuteProcess(main_args, NULL, NULL);
  if (exit_code >= 0) {
    return exit_code;
  }

  XSetErrorHandler(XErrorHandlerImpl);
  XSetIOErrorHandler(XIOErrorHandlerImpl);
  CefEnableHighDPISupport();

  CefSettings settings;
  settings.log_severity = LOGSEVERITY_ERROR;
  settings.no_sandbox = true;

  CefRefPtr<PyNodeApp> app(new PyNodeApp);
  CefInitialize(main_args, settings, app.get(), NULL);
  
  CefRunMessageLoop();
  CefShutdown();

  return 0;
}
