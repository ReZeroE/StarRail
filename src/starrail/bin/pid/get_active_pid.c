// Compile: 
//    gcc .\get_active_pid.c -o ../get_active_pid

#include <windows.h>
#include <stdio.h>

int main() {
    DWORD pid;
    HWND hwnd = GetForegroundWindow();      // get handle of currently active window
    if (hwnd == NULL) {
        printf("No active window\n");
        return 1;
    }

    GetWindowThreadProcessId(hwnd, &pid);   // get PID
    // printf("Active window PID: %lu\n", pid);
    printf("%lu\n", pid);

    return 0;
}