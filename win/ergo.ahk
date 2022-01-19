#NoEnv  ; Recommended for performance and compatibility with future AutoHotkey releases.
; #Warn  ; Enable warnings to assist with detecting common errors.
SendMode Input  ; Recommended for new scripts due to its superior speed and reliability.
SetWorkingDir %A_ScriptDir%  ; Ensures a consistent starting directory.

SetCapsLockState, AlwaysOff

#If GetKeyState("CapsLock" , "P")

n::left
н::left
u::up
у::up
e::down
е::down
o::right
о::right
t::shift
т::shift
h::ctrl
ч::ctrl
s::alt
с::alt

m::^c
м::^c
c::^v
ц::^v
x::^x
х::^x
z::^z
з::^z
a::^a
а::^a
k::PgDn
к::PgDn
y::PgUp
ы::PgUp

,::Esc
Space::Tab

#If


::gitcp::git commit -am up && git push