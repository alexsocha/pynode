// Copyright (c) 2017 Alex Socha
// https://alexsocha.github.io/pynode

#ifndef CEF_PYNODE_PYNODE_HANDLER_H_
#define CEF_PYNODE_PYNODE_HANDLER_H_

#include "include/cef_client.h"

#include <list>

class PyNodeHandler : public CefClient, public CefDisplayHandler, public CefLifeSpanHandler, public CefLoadHandler, public CefRequestHandler, public CefContextMenuHandler
{
public:
	explicit PyNodeHandler(bool use_views);
	~PyNodeHandler();
	static PyNodeHandler* GetInstance();
	virtual CefRefPtr<CefBrowser> GetBrowser();

	// CefClient methods:
	virtual CefRefPtr<CefDisplayHandler> GetDisplayHandler() OVERRIDE { return this; }
	virtual CefRefPtr<CefLifeSpanHandler> GetLifeSpanHandler() OVERRIDE { return this; }
	virtual CefRefPtr<CefLoadHandler> GetLoadHandler() OVERRIDE { return this; }
	virtual CefRefPtr<CefRequestHandler> GetRequestHandler() OVERRIDE { return this; }
	virtual CefRefPtr<CefContextMenuHandler> GetContextMenuHandler() OVERRIDE { return this; }

	// CefDisplayHandler methods:
	virtual void OnTitleChange(CefRefPtr<CefBrowser> browser, const CefString& title) OVERRIDE;
	virtual bool OnConsoleMessage(CefRefPtr<CefBrowser> browser, const CefString& message, const CefString& source, int line) OVERRIDE;

	// CefLifeSpanHandler methods:
	virtual void OnAfterCreated(CefRefPtr<CefBrowser> browser) OVERRIDE;
	virtual bool DoClose(CefRefPtr<CefBrowser> browser) OVERRIDE;
	virtual void OnBeforeClose(CefRefPtr<CefBrowser> browser) OVERRIDE;

	// CefLoadHandler methods:
	virtual void OnLoadError(CefRefPtr<CefBrowser> browser, CefRefPtr<CefFrame> frame, ErrorCode errorCode, const CefString& errorText, const CefString& failedUrl) OVERRIDE;
	void CloseAllBrowsers(bool force_close);
	bool IsClosing() const { return is_closing_; }

	// CefRequestHandler methods:
	virtual bool OnBeforeBrowse(CefRefPtr<CefBrowser> browser, CefRefPtr<CefFrame> frame, CefRefPtr<CefRequest> request, bool is_redirect) OVERRIDE;

	// CefContextMenuHandler methods:
	virtual void OnBeforeContextMenu(CefRefPtr<CefBrowser> browser, CefRefPtr<CefFrame> frame, CefRefPtr<CefContextMenuParams> params, CefRefPtr<CefMenuModel> model) OVERRIDE;
	virtual bool OnContextMenuCommand(CefRefPtr<CefBrowser> browser, CefRefPtr<CefFrame> frame, CefRefPtr<CefContextMenuParams> params, int command_id, CefContextMenuHandler::EventFlags event_flags) OVERRIDE;

private:
	void PlatformTitleChange(CefRefPtr<CefBrowser> browser, const CefString& title);
	const bool use_views_;

	typedef std::list<CefRefPtr<CefBrowser> > BrowserList;
	BrowserList browser_list_;
	bool is_closing_;

	IMPLEMENT_REFCOUNTING(PyNodeHandler);
};

#endif
