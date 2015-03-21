random musings
==============

the purpose of this file is just to jot down thoughts related to the goals and
scope of the pygame2 project.  none of this is to be taken as a hard truth or
strong commitment, rather just a place to brainstorm ideas.


developer experience
====================

pygame2 should preserve the raw thrills of pygame, while offering a clear path
to actually do something useful with it.  what i mean, specifically, is 
preserving the ability to 'build a game engine', or make your first jrpg.

it should be usable as a prototyping kit, like a box of legos, but it also
needs strong tools to make a game/app that will work like modern apps do.

pygame vetrans will think fondly of the wall that everyone hits once they
realize that pygame apps do not scale.  pygame2 should scale.  100's of
on-screen sprites should work.  we don't want to bother with calling convert
on images we load...

pygame2 should let you cut your teeth on some low level details, but when you
want the low level stuff to be taken care of, pygame2 should ship with
sensible tools like event dispatchers, resource loaders, and input abstractions.

the general idea that pygame2 should be useful to use, and useful
to teach with demands a lot of reusable abstractions.

here is a sample pygame2 newbie:
* wants to 'see' events from the queue and directly manage them
* wants to directly control when and where things are on the screen
* wants to directly call functions on sprites/sprite-objects
* probably wants to use a vanilla list or set to mange sprites
* doesn't want 'game engine magic'
* wants to handle things with 'for loops'

here is a sample pygame2 veteran:
* lets pygame2.app.App do all of the boring work
* uses decorator and event framework
* organizes things into batches/groups
* lets 'game engine magic' do heavy lifting
* uses callbacks, scheduler, and generators

As an aside, the pygame2 veteran will also want to do some things
a newbie would want, such as directly controlling the event queue,
so by catering to both groups, the library is more usable.


modern features
===============

pygame2 should be able to use 2d physics engines and open source editors.
it will ship with pyopengl as a first class citizen, along with useful places
to extend pygame2 with custom shaders and opengl code.
