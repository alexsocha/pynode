// Copyright (c) 2017 Alex Socha
// http://www.alexsocha.com/pynode

#include "pynode_handler.h"
#include "pynode_app.h"
#include "resource.h"

#include <sstream>
#include <string>
#include <iostream>
#if defined(OS_WIN)
	#include <ShellAPI.h>
#endif
#if defined(OS_MACOSX)
	#include <ApplicationServices/ApplicationServices.h>
	#import <Carbon/Carbon.h>
#endif
#if defined(OS_LINUX)
	#include <X11/Xlib.h>
	#include <X11/Xutil.h>
	#include <thread>
#endif
#include "include/base/cef_bind.h"
#include "include/cef_app.h"
#include "include/views/cef_browser_view.h"
#include "include/views/cef_window.h"
#include "include/wrapper/cef_closure_task.h"
#include "include/wrapper/cef_helpers.h"

#define ID_CONTEXT_MENU_ABOUT_PYNODE 122

namespace {
    PyNodeHandler* g_instance = NULL;
}

PyNodeHandler::PyNodeHandler(bool use_views) : use_views_(use_views), is_closing_(false) {
    DCHECK(!g_instance);
    g_instance = this;
}

PyNodeHandler::~PyNodeHandler() {
    g_instance = NULL;
}

PyNodeHandler* PyNodeHandler::GetInstance() {
    return g_instance;
}

CefRefPtr<CefBrowser> PyNodeHandler::GetBrowser() {
    if (browser_list_.empty()) return NULL;
    return browser_list_.front();
}

bool PyNodeHandler::OnConsoleMessage(CefRefPtr<CefBrowser> browser, const CefString& message, const CefString &source, int line) {
    return PyNodeApp::RecieveJavaScript(message.ToString());
}

void PyNodeHandler::OnTitleChange(CefRefPtr<CefBrowser> browser, const CefString& title) {
    CEF_REQUIRE_UI_THREAD();
    if (use_views_) {
        CefRefPtr<CefBrowserView> browser_view = CefBrowserView::GetForBrowser(browser);
        if (browser_view) {
            CefRefPtr<CefWindow> window = browser_view->GetWindow();
            if (window)
                window->SetTitle(title);
        }
    } else {
        PlatformTitleChange(browser, title);
    }
}

bool PyNodeHandler::OnBeforeBrowse(CefRefPtr<CefBrowser> browser, CefRefPtr<CefFrame> frame, CefRefPtr<CefRequest> request, bool is_redirect) {
	CEF_REQUIRE_UI_THREAD();
	CefString url = request->GetURL();
	std::string prefix = "http";
	if (url.ToString().substr(0, prefix.size()) == prefix) {
#if defined(OS_WIN)
		ShellExecute(NULL, CefString("open").c_str(), url.c_str(), NULL, NULL, SW_SHOWNORMAL);
#endif
#if defined(OS_MACOSX)
		system(("open " + url.ToString()).c_str());
#endif
		return true;
	}
	return false;
}

void PyNodeHandler::OnBeforeContextMenu(CefRefPtr<CefBrowser> browser, CefRefPtr<CefFrame> frame, CefRefPtr<CefContextMenuParams> params, CefRefPtr<CefMenuModel> model) {
	CEF_REQUIRE_UI_THREAD();
	model->Clear();
	model->AddItem(ID_CONTEXT_MENU_ABOUT_PYNODE, "About PyNode");
}

#if defined(OS_WIN)
INT_PTR CALLBACK AboutDlgProc(HWND hwnd, UINT Message, WPARAM wParam, LPARAM lParam) {
	switch (Message)
	{
	case WM_INITDIALOG:
		return TRUE;
	case WM_COMMAND:
		EndDialog(hwnd, NULL);
		break;
	default:
		return FALSE;
	}
	return TRUE;
}
#endif

bool PyNodeHandler::OnContextMenuCommand(CefRefPtr<CefBrowser> browser, CefRefPtr<CefFrame> frame, CefRefPtr<CefContextMenuParams> params, int command_id, CefContextMenuHandler::EventFlags event_flags) {
	if (command_id == ID_CONTEXT_MENU_ABOUT_PYNODE) {
#if defined(OS_WIN)
	CreateDialog(GetModuleHandle(NULL), MAKEINTRESOURCE(IDD_ABOUT_DIALOG), browser->GetHost()->GetWindowHandle(), AboutDlgProc);
	return true;
#endif
#if defined(OS_MACOSX)
        CGEventSourceRef source = CGEventSourceCreate(kCGEventSourceStateCombinedSessionState);
        CGEventRef aboutCommandDown = CGEventCreateKeyboardEvent(source, kVK_ANSI_A, TRUE);
        CGEventSetFlags(aboutCommandDown, kCGEventFlagMaskCommand);
        CGEventRef aboutCommandUp = CGEventCreateKeyboardEvent(source, kVK_ANSI_A, FALSE);
        CGEventPost(kCGAnnotatedSessionEventTap, aboutCommandDown);
        CGEventPost(kCGAnnotatedSessionEventTap, aboutCommandUp);
        CFRelease(aboutCommandUp);
        CFRelease(aboutCommandDown);
        CFRelease(source);
        return true;
#endif
#if defined(OS_LINUX)
	
std::thread t([](){
	Display *dpy = XOpenDisplay(NULL);
	int blackColor = BlackPixel(dpy, DefaultScreen(dpy));
	int whiteColor = WhitePixel(dpy, DefaultScreen(dpy));
	Screen* screen = DefaultScreenOfDisplay(dpy);
	int windowWidth = 210;
	int windowHeight = 100;
	int windowX = (screen->width / 2) - (windowWidth / 2);
	int windowY = (screen->height / 2) - (windowHeight / 2);
	Window w = XCreateSimpleWindow(dpy, DefaultRootWindow(dpy), windowX, windowY, 
				windowWidth, windowHeight, 1, blackColor, whiteColor);
	XMapWindow(dpy, w);
	GC gc = XCreateGC(dpy, w, 0, 0);
	XSelectInput(dpy, w, ExposureMask | KeyPressMask);
	
	XSizeHints wmsize;
	wmsize.flags = USPosition | PMinSize | PMaxSize;
	wmsize.x = windowX; wmsize.y = windowY;
	wmsize.min_width = windowWidth; wmsize.min_height = windowHeight;
	wmsize.max_width = windowWidth; wmsize.max_height = windowHeight;
	XSetWMNormalHints(dpy, w, &wmsize);
	
	XStoreName(dpy, w, "About PyNode");
	
	Atom WM_DELETE_WINDOW = XInternAtom(dpy, "WM_DELETE_WINDOW", False); 
	XSetWMProtocols(dpy, w, &WM_DELETE_WINDOW, 1);
	XEvent e;
	const char *msg1 = "About PyNode";
	const char *msg2 = "Copyright \xa9 Alex Socha 2017";
	const char *msg3 = "http://www.alexsocha.com/pynode";
	while (1) {
		XNextEvent(dpy, &e);
		if (e.type == Expose) {
			XDrawString(dpy, w, gc, 10, 30, msg1, strlen(msg1));
			XDrawString(dpy, w, gc, 10, 50, msg2, strlen(msg2));
			XDrawString(dpy, w, gc, 10, 70, msg3, strlen(msg3));
		}
		else if (e.type == KeyPress)
			break;
		else if (e.type == ClientMessage)
			break;
	}
	XCloseDisplay(dpy);
    });
    t.detach();
#endif
    }
	return false;
}

void PyNodeHandler::OnAfterCreated(CefRefPtr<CefBrowser> browser) {
    CEF_REQUIRE_UI_THREAD();
#if defined(OS_WIN)
	HICON hIcon = static_cast<HICON>(LoadIcon(GetModuleHandle(NULL), MAKEINTRESOURCE(IDI_PYNODE)));
	HICON hIconSmall = static_cast<HICON>(LoadIcon(GetModuleHandle(NULL), MAKEINTRESOURCE(IDI_SMALL)));
	if (hIcon) SendMessage(browser->GetHost()->GetWindowHandle(), WM_SETICON, ICON_BIG, (LPARAM)hIcon);
	if (hIconSmall) SendMessage(browser->GetHost()->GetWindowHandle(), WM_SETICON, ICON_SMALL, (LPARAM)hIconSmall);
#endif

    browser_list_.push_back(browser);
}

bool PyNodeHandler::DoClose(CefRefPtr<CefBrowser> browser) {
    CEF_REQUIRE_UI_THREAD();
    if (browser_list_.size() == 1) is_closing_ = true;
    return false;
}

void PyNodeHandler::OnBeforeClose(CefRefPtr<CefBrowser> browser) {
    CEF_REQUIRE_UI_THREAD();

	std::cout << "pynode:exit" << std::endl;
    
    BrowserList::iterator bit = browser_list_.begin();
    for (; bit != browser_list_.end(); ++bit) {
        if ((*bit)->IsSame(browser)) {
            browser_list_.erase(bit);
            break;
        }
    }
    if (browser_list_.empty()) CefQuitMessageLoop();
}

void PyNodeHandler::OnLoadError(CefRefPtr<CefBrowser> browser, CefRefPtr<CefFrame> frame, ErrorCode errorCode, const CefString& errorText, const CefString& failedUrl) {
    CEF_REQUIRE_UI_THREAD();
    if (errorCode == ERR_ABORTED) return;
    std::stringstream ss;
    ss << "<html><body bgcolor=\"white\">"
    "<h2>Failed to load URL " << std::string(failedUrl) <<
    " with error " << std::string(errorText) << " (" << errorCode <<
    ").</h2></body></html>";
    frame->LoadString(ss.str(), failedUrl);
}

void PyNodeHandler::CloseAllBrowsers(bool force_close) {
    if (!CefCurrentlyOn(TID_UI)) {
        CefPostTask(TID_UI, base::Bind(&PyNodeHandler::CloseAllBrowsers, this, force_close));
        return;
    }
    if (browser_list_.empty()) return;
    
    BrowserList::const_iterator it = browser_list_.begin();
    for (; it != browser_list_.end(); ++it)
        (*it)->GetHost()->CloseBrowser(force_close);
}
