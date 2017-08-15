// Copyright (c) 2017 Alex Socha
// http://www.alexsocha.com/pynode

#include "pynode_handler.h"

#include <string>
#include <windows.h>

#include "include/cef_browser.h"

void PyNodeHandler::PlatformTitleChange(CefRefPtr<CefBrowser> browser, const CefString& title)
{
	CefWindowHandle hwnd = browser->GetHost()->GetWindowHandle();
	CefString new_title = "PyNode";
	SetWindowText(hwnd, new_title.c_str());
}
