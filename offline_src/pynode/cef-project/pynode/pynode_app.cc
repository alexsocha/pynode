// Copyright (c) 2017 Alex Socha
// http://www.alexsocha.com/pynode

#include "pynode_app.h"

#include <string>
#include <stdlib.h>
#include <stdio.h>
#include <iostream>
#include <fstream>
#include <limits.h>
#include <thread>

#if defined(OS_MACOSX)
	#include <ApplicationServices/ApplicationServices.h>
#endif
#if defined(OS_WIN)
	#include <windows.h>
#endif
#if defined(OS_LINUX)
	#include <X11/Xlib.h>
#endif

#include "pynode_handler.h"
#include "include/cef_browser.h"
#include "include/cef_command_line.h"
#include "include/views/cef_browser_view.h"
#include "include/views/cef_window.h"
#include "include/wrapper/cef_helpers.h"

// The location of the main.py file
#define PYNODEPATH "."

namespace
{
	class PyNodeWindowDelegate : public CefWindowDelegate
	{
	public:
		explicit PyNodeWindowDelegate(CefRefPtr<CefBrowserView> browser_view) : browser_view_(browser_view) {}

		void OnWindowCreated(CefRefPtr<CefWindow> window) OVERRIDE
		{
			window->AddChildView(browser_view_);
			window->Show();
		}

		void OnWindowDestroyed(CefRefPtr<CefWindow> window) OVERRIDE
		{
			browser_view_ = NULL;
		}

		bool CanClose(CefRefPtr<CefWindow> window) OVERRIDE
		{
			CefRefPtr<CefBrowser> browser = browser_view_->GetBrowser();
			if (browser) return browser->GetHost()->TryCloseBrowser();
			return true;
		}

	private:
		CefRefPtr<CefBrowserView> browser_view_;

		IMPLEMENT_REFCOUNTING(PyNodeWindowDelegate);
		DISALLOW_COPY_AND_ASSIGN(PyNodeWindowDelegate);
	};
}

void MonitorPython(std::string arg)
{
	while (true)
	{
		if (PyNodeHandler::GetInstance() && PyNodeHandler::GetInstance()->GetBrowser())
		{
			std::string message;
			std::getline(std::cin, message);
			if (message.find("pynode:") == 0)
			{
				std::string data = message.substr(7);
				std::string function = data.substr(0, data.find(':'));
				std::string args = data.substr(data.find(':') + 1);
				PyNodeHandler::GetInstance()->GetBrowser()->GetMainFrame()->ExecuteJavaScript("js_run_function('" + function + "', '" + args + "');", PyNodeHandler::GetInstance()->GetBrowser()->GetMainFrame()->GetURL(), 0);
			}
		}
		else
		{
			std::this_thread::sleep_for(std::chrono::milliseconds(100));
		}
	}
}

bool PyNodeApp::RecieveJavaScript(std::string message)
{
	if (message.find("pynode:") == 0)
	{
		std::cout << message << std::endl;
		return true;
	}
	return false;
}

PyNodeApp::PyNodeApp() {}

void PyNodeApp::OnContextInitialized()
{
	CEF_REQUIRE_UI_THREAD();

	CefRefPtr<CefCommandLine> command_line = CefCommandLine::GetGlobalCommandLine();
	CefRefPtr<PyNodeHandler> handler(new PyNodeHandler(false));
	CefBrowserSettings browser_settings;

	CefString path = PYNODEPATH "/src/html/pynode_output.html";
	CefString absulote_path;
	
#if defined(OS_MACOSX)
	char buffer[PATH_MAX + 1];
	absulote_path = realpath(path.ToString().c_str(), buffer);
#endif
#if defined(OS_WIN)
	wchar_t buffer[MAX_PATH + 1];
	GetFullPathName(path.c_str(), 234, buffer, NULL);
	absulote_path = buffer;
#endif
#if defined(OS_LINUX)
	char buffer[PATH_MAX + 1];
	absulote_path = realpath(path.ToString().c_str(), buffer);
#endif
	CefString url = "file://" + absulote_path.ToString();
	CefWindowInfo window_info;
	int window_width = 600, window_height = 600;
	
#if defined(OS_MACOSX)
	window_info.width = window_width;
	window_info.height = window_height;
	window_info.x = (CGDisplayPixelsWide(CGMainDisplayID()) / 2) - (window_width / 2);
	window_info.y = (CGDisplayPixelsHigh(CGMainDisplayID()) / 2) + (window_height / 2);
#endif

#if defined(OS_WIN)
	window_info.SetAsPopup(NULL, "PyNode");
	window_info.width = window_width;
	window_info.height = window_height;
	window_info.x = (GetSystemMetrics(SM_CXSCREEN) / 2) - (window_width / 2);
	window_info.y = (GetSystemMetrics(SM_CYSCREEN) / 2) - (window_height / 2);
#endif

#if defined(OS_LINUX)
	window_info.width = window_width;
	window_info.height = window_height;
	Display* disp = XOpenDisplay(NULL);
	Screen* screen = DefaultScreenOfDisplay(disp);
	window_info.x = (screen->width / 2) - (window_width / 2);
	window_info.y = (screen->height / 2) - (window_height / 2);
#endif
	
	CefBrowserHost::CreateBrowser(window_info, handler, url, browser_settings, NULL);

	std::thread monitor_thread(MonitorPython, "");
	monitor_thread.detach();
}
