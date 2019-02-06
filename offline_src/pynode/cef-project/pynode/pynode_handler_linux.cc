// Copyright (c) 2017 Alex Socha
// https://alexsocha.github.io/pynode

#include "pynode_handler.h"

#include <X11/Xatom.h>
#include <X11/Xlib.h>
#include <string>

#include "include/base/cef_logging.h"
#include "include/cef_browser.h"

void PyNodeHandler::PlatformTitleChange(CefRefPtr<CefBrowser> browser,
                                        const CefString& title) {
  std::string titleStr("PyNode");

  ::Display* display = cef_get_xdisplay();
  DCHECK(display);

  ::Window window = browser->GetHost()->GetWindowHandle();
  DCHECK(window != kNullWindowHandle);

  const char* kAtoms[] = {
    "_NET_WM_NAME",
    "UTF8_STRING"
  };
  Atom atoms[2];
  int result = XInternAtoms(display, const_cast<char**>(kAtoms), 2, false, atoms);
  if (!result) NOTREACHED();

  XChangeProperty(display, window, atoms[0], atoms[1], 8, PropModeReplace,
                  reinterpret_cast<const unsigned char*>(titleStr.c_str()), titleStr.size());
  XStoreName(display, browser->GetHost()->GetWindowHandle(), titleStr.c_str());
}

