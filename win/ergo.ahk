#NoEnv  ; Recommended for performance and compatibility with future AutoHotkey releases.
; #Warn  ; Enable warnings to assist with detecting common errors.
SendMode Input  ; Recommended for new scripts due to its superior speed and reliability.
SetWorkingDir %A_ScriptDir%  ; Ensures a consistent starting directory.

#KeyHistory 500

SetCapsLockState, AlwaysOff

; -----------------------------------------------------------------------
; Within CapsLock context
#if GetKeyState("CapsLock" , "P")

SC01E::^a    ; a
SC01F::alt   ; s
SC020::ctrl  ; d
SC021::shift ; f

SC016::home  ; u
SC017::up    ; i
SC018::end   ; o

SC024::left  ; j
SC025::down  ; k
SC026::right ; l
SC027::enter ; ;

SC02D::^x    ; x
SC02E::^c    ; c
SC02F::^v    ; v

SC023::PgUp  ; h
SC031::PgDn  ; n

SC02C::^z    ; z

SC032::backspace ; m
SC033::Esc       ; ,
SC034::delete    ; .


SC039::Tab   ; space

; -----------------------------------------------------------------------
; Without context
#If
CapsLock up::
	Send {Shift up}{Ctrl up}{Alt up}
	; ToolTip CapsLock %cs_state%

	
::gitcp::git commit -am up && git push

