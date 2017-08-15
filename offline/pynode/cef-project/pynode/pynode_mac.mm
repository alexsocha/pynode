// Copyright (c) 2017 Alex Socha

#import <Cocoa/Cocoa.h>

#include "pynode_app.h"
#include "pynode_handler.h"
#include "include/cef_application_mac.h"
#include "include/wrapper/cef_helpers.h"

@interface PyNodeAppDelegate : NSObject<NSApplicationDelegate>
- (void)createApplication:(id)object;
- (void)tryToTerminateApplication:(NSApplication*)app;
@end

@interface PyNodeApplication : NSApplication<CefAppProtocol> {
@private
    BOOL handlingSendEvent_;
}
@end

@implementation PyNodeApplication
- (BOOL)isHandlingSendEvent {
    return handlingSendEvent_;
}

- (void)setHandlingSendEvent:(BOOL)handlingSendEvent {
    handlingSendEvent_ = handlingSendEvent;
}

- (void)sendEvent:(NSEvent*)event {
    CefScopedSendingEvent sendingEventScoper;
    [super sendEvent:event];
}

- (void)terminate:(id)sender {
    PyNodeAppDelegate* delegate = static_cast<PyNodeAppDelegate*>([NSApp delegate]);
    [delegate tryToTerminateApplication:self];
}
@end

@implementation PyNodeAppDelegate

- (void)createApplication:(id)object {
    [NSApplication sharedApplication];
    [[NSBundle mainBundle] loadNibNamed:@"MainMenu" owner:NSApp topLevelObjects:nil];
    [[NSApplication sharedApplication] setDelegate:self];
}

- (void)tryToTerminateApplication:(NSApplication*)app {
    PyNodeHandler* handler = PyNodeHandler::GetInstance();
    if (handler && !handler->IsClosing()) handler->CloseAllBrowsers(false);
}

- (NSApplicationTerminateReply)applicationShouldTerminate:
(NSApplication *)sender {
    return NSTerminateNow;
}
@end

int main(int argc, char* argv[]) {
    CefMainArgs main_args(argc, argv);
    NSAutoreleasePool* autopool = [[NSAutoreleasePool alloc] init];
    [PyNodeApplication sharedApplication];
    
    CefSettings settings;
    settings.log_severity = LOGSEVERITY_ERROR;
    
    CefRefPtr<PyNodeApp> app(new PyNodeApp);
    CefInitialize(main_args, settings, app.get(), NULL);
    NSObject* delegate = [[PyNodeAppDelegate alloc] init];
    [delegate performSelectorOnMainThread:@selector(createApplication:) withObject:nil waitUntilDone:NO];
    
    CefRunMessageLoop();
    CefShutdown();
    
    [delegate release];
    [autopool release];
    
    return 0;
}
