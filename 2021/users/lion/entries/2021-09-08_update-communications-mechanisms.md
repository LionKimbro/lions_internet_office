# Update Communication Mechanisms
Lion Kimbro
2021-09-08

## <a name="context">Context</a>
I've been advocating for "transparent" data systems (I'm just now making up that term) -- wherein the data used by one application is also routinely used by other applications as well -- whether or not the executables associated with that application are running or not.

Ciprian Cracium and I have been talking about this in [Lion's Internet Office on Discord](https://discord.gg/V8wDBh8d), and [Ciprian brought up the idea of using such with an outliner or tree organizer tool.](https://scratchpad.volution.ro/ciprian/992c7f2944456f18cdde77f683f49aa7/6697ebb3.html)

The subject came up:  "If there's a program that's actively making use of the data, how does it get notified of changes from other programs?"

## <a name="changefiles">Advocacy: Unique Change Files</a>

In this article, I advocate for a specific mechanism:  Have a directory where change notifications are posted to, and then the program actively using the data scans that directory for changes that it is interested in.

### <a name="fileformat">File Format</a>

The file would look something like so:

    C:\Users\Lion\my-notes\node3845\children\node4965\title.txt
    C:\Users\Lion\my-notes\node3856\children\node4965\data\

That is, it's just a text file (UTF-8 encoded,) and each line is a path to a file or to a directory.

In the example here, there are two things notified:
* the particular node's title was changed
* the particular node's data was updated

It's not critical that all information about the update is provided -- whether it's a delete, an update, an addition, whatever -- it'll be up to the program reading the changes to investigate the situation, and update local memory in response.

### <a name="filenames">Unique Filenames</a>

That's what the file looks like -- where does it go?

Presumably, there is some folder somewhere, that change notifications go into.  Several different data collections could share a single change-notification folder, or perhaps there's just one folder per data collection.  It doesn't matter; Just that the program that needs to be monitoring for changes, and the program that is making the changes, know to read and publish in the same place.

Unique filenames are necessary so that two non-communicating processes don't clobber one another.  Unique filenames could be created with a v4 UUID, they could be created from 3-tuple PID, process start time, & serial number.  All that really matters, though, is that the filenames are unique.

***Addendum, 2021-09-09 1:11a Seattle:** Ciprian points out that PID+time is not unique if the filesystem is shared and different systems can touch the directory space.  At this point, you'd need to add in the MAC address or some other unique identifier of the computer itself.*

So the filename for the change update might just be:

    C:\Users\Lion\my-notes\notifications\92e64607-7858-45e3-8806-184a95d678e1.txt

The filename might be:

    C:\Users\Lion\my-notes\notifications\687756_613986c8_0.txt

(In that case, it would be: PID# 687756, process created 0x613986c8 seconds since the epoch, serial number #0.)

I like the traceability of the latter, but the former is easier to write code for.

## <a name="other-mechanisms">Other Mechanisms Discussed</a>

The primary competing mechanisms are as follows:

### <a name="scanning">Scanning All Files for Changes</a>

That is, a process that is actively and continuously working with the tree, would look at all of the files in the tree, and see if there are any changes to them.  Did the modified timestamp change?  Or perhaps a hash of the file has changed?

My concern with this method is that I don't think it will scale well.

I have data sets that easily have 10,000 items in them, and if each node has roughly 10 files within it, then that's on the order of 100,000 files that need to be scanned on a regular interval.

The temptation would be to lengthen out the intervals, but then that means that the user is confused why, after 10 seconds, a change hasn't showed up in the user interface yet.

(I'd be worried about the user making conflicting changes within those 10 seconds, but then I realized that the program can verify the path up to where the user is making edits, as the user edits, -- just assuming that there may have been changes in that area.  So that would be caught before the user's change was issued.  Therefore, the issue is primarily about rapidly notifying the user of changes that are made by other programs.)

### <a name="os-monitor">Use an OS/Filesystem Level Monitor</a>

There are APIs for most operating systems and filesystems now, I understand, for getting notification that a file has changed.

For example, there is this article:
* [Time Golden's Python Stuff: Watch a Directory for Changes](http://timgolden.me.uk/python/win32_how_do_i/watch_directory_for_changes.html) 

Outside of polling directories, you find yourself in OS-dependent code, and it's a lot of work.

For myself, I find that I don't quite trust it.  For example, I regularly work on both Linux and Windows systems, and I share the same code between the two systems.  Do I really want to write, test, and maintain two different sets of code for the two different systems?

And what happens if Windows changes their API, or Linux changes their API, or Macintosh changes their API?

I don't want to have to think about that.

## <a name="summary">Summary & Conclusion</a>

* Record Change Notifications
  * +: very simple to write
  * +: very simple to interpret
  * +: changes are picked up relatively quickly
  * +: works on all operating systems
  * +: you only have to poll x1 directory for change notifications
  * -: you DO have to poll a directory for change notifications
  * -: changing programs must write notifications
  * -: you have to periodically get rid of old notifications
  * -: changes made manually (perhaps via, say, notepad.exe,) will not be picked up, unless the user manually creates a change notice
 * Scanning for Changes
   * +: no changes will go unnoticed
   * +: programs that make changes to the data have no burden
   * +: works on all operating systems, (provided you can get file metadata)
   * -: the code is more complicated
   * -: scales poorly: you have to repeatedly poll all files
   * -: scales poorly: there's a lot of in-memory book-keeping to do
 * Monitor Files for Changes with OS/Filesystem APIs
   * +: no changes will go unnoticed
   * +: changes are picked up nearly instantaneously
   * +: programs that make changes to the data have no burden
   * -: the code is more complicated
   * -: require OS-dependent code & testing for each OS

This may be more of an aesthetic question, but for myself, I generally prefer "low-tech" to "high-tech."  The basic operations of listing files in a directory, opening and reading files, are accessible to just about everybody.

I think that is a program is designed to operate within another program's data collection, then it is reasonable that it be asked to create a file and tip the other program off to: "Hey, I did something here."

This said, if you are performing global search and replaces, and not getting "Hey, here's the files I touched" in response, then that is an argument back in favor of period scans or OS-level file monitoring.

And then on the other hand again, you could just trigger a total reload, either by a direct command within the program, or creating a file that simply says, "the entirety of the project was changed."  (Addressing the root node.)

## <a name="watchexec">Addendum #1: WatchExec</a>

Ciprian points out that there is a tool called [watchexec](https://github.com/watchexec/watchexec) that can perform file monitoring, and then run a program when it detects a change.

Just glancing through the watchexec documentation, I see that it could be easily adapted to produce the unique change files.

This would mean that all changes would be picked up, and this would mean that changing programs would not have to write notifications.

Interesting!

## <a name="changelog">Addendum #2: Fuller ChangeLog<a>

> "It is a good idea to also catch change notifications somehow. ... On the other hand, how about renaming the `notifications` folder to something like `changelog`, let it be permanent, and structure it with fields similar to what is needed by an RSS feed (author like you've proposed, path, title, perhaps a diff); (the process ID is not much worth;) now one can easily create an RSS feed from this without other inputs." -- Ciprian

This is also an interesting idea.  Rather than just sending the path to the changed file, supply a whole lot of information.

I can imagine sending the following information, immediately:
* the path to the file that was changed
* a logical identifier for the data that was changed (perhaps a node#, or something)
* when the change was made
* the type of change that was made (create, delete, update)
* information on how to undo the change
* information on the process that made the change
    * the PID for the process
	* how to communicate back to the process that made the change
	* the kind of process that it is
	* human readable information about the process, for presentation
	* the active human agent behind the process
