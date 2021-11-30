#NoEnv  ; Recommended for performance and compatibility with future AutoHotkey releases.
; #Warn  ; Enable warnings to assist with detecting common errors.
SendMode Input  ; Recommended for new scripts due to its superior speed and reliability.
SetWorkingDir %A_ScriptDir%  ; Ensures a consistent starting directory.

SetCapsLockState, AlwaysOff

#If GetKeyState("CapsLock" , "P")

n::left
u::up
e::down
o::right
t::shift
h::ctrl
s::alt

m::^c
c::^v
x::^x
z::^z
a::^a
k::PgDn
y::PgUp

,::Esc
Space::Tab

#If


::gitcp::git commit -am up && git push