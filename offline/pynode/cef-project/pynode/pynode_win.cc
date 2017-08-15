// Copyright (c) 2017 Alex Socha
// http://www.alexsocha.com/pynode

#include <windows.h>
#include "pynode_app.h"
#include "resource.h"


// Entry point function for all processes.
int APIENTRY wWinMain(HINSTANCE hInstance, HINSTANCE hPrevInstance, LPTSTR lpCmdLine, int nCmdShow)
{
	UNREFERENCED_PARAMETER(hPrevInstance);
	UNREFERENCED_PARAMETER(lpCmdLine);
	CefEnableHighDPISupport();

	CefMainArgs main_args(hInstance);
	int exit_code = CefExecuteProcess(main_args, NULL, NULL);
	if (exit_code >= 0)
		return exit_code;

	CefSettings settings;
	settings.log_severity = LOGSEVERITY_ERROR;
	settings.no_sandbox = true;

	CefRefPtr<PyNodeApp> app(new PyNodeApp);
	CefInitialize(main_args, settings, app.get(), NULL);

	CefRunMessageLoop();
	CefShutdown();

	return 0;
}
