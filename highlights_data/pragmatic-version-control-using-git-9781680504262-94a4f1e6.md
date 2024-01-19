---
asset_id: 94A4F1E61B64D158738DF5CD1DC2F380
author: Swicegood Travis
modified_date: '2023-12-26T14:38:23'
title: Pragmatic Version Control Using Git 9781680504262
---

# Pragmatic Version Control Using Git 9781680504262

By Swicegood Travis

## My notes <a name="my_notes_dont_delete"></a>



## iBooks notes <a name="ibooks_notes_dont_delete"></a>

            First, you have only the latest version of the code.  To look at
            the history of changes, you have to ask the repository for that information.
        

            That brings up the second problem.  You have to be able to access the remote
            repository—normally over a network.

That highlights one of the biggest advantages of a DVCS, which is the model that Git follows.  Instead of having one
            central repository that you and everyone else on your team sends changes
            to, you each have your own repository that has the entire history of the project.
            Making a commit doesn’t involve connecting to a remote repository; the change
            is recorded in your local repository.

Determining what to include is easy. Ask yourself, “If I didn’t
            have X, could I do my work on this project?” If the answer is no, 
            you couldn’t, then it should be included.

working tree—your current
            view of the repository

There are two steps to retrieving changes from a remote Git repository.
            First, you fetch them.  That creates a copy of the remote repository’s
            changes for you.  This step is sort of like the reverse of pushing.
            Instead of sending changes to another repository, you ask the remote
            repository to send you the changes it has.
        

            Next, you merge those changes into your local history.  Git
            provides tools that help you merge changes.  Since you normally want to
            fetch and merge changes at the same time, Git provides a way to do both
            in one step through a process called pulling.
            Pulling is similar to an update command in Subversion or CVS.
        

            

            Instead of tracking a models.py file,
            Git tracks the content—the individual characters and lines
            that make up the variables, functions, and so on—of
            models.py, and Git adds
            metadata to it such as the name, file mode, and whether the file is a symlink.
            It’s a nuanced difference, but it’s an important one.

Either way, you need to keep track of what state
            your repository was in when you passed that milestone.  Tags
            give us the tool to do that.  They mark a certain point
            in the history of the repository so you can easily reference
            them later.
        

            A tag is simply a name that you can use to mark some specific
            point in the repository’s history.  It can be a major milestone
            such as a public release or something much more routine like
            the point at which a bug was fixed in your repository.

Tags help you keep track of the history of your repository by
            assigning an easy-to-remember name to a certain revision

This is where branches come in.  You can create a branch that
            marks a point where the files in the
            repository diverged.  Each branch keeps track of the changes
            made to its content separately from other branches so you
            can create alternate histories.
        

            

The branch can exist for the rest of the project or for just a few hours.
            It can be merged into another branch, but there’s no hard rule
            saying a branch has to be merged.
        

            Sometimes, you don’t even want them to merge.  It might be a
            branch to track an older major version of your project, or
            it could be an experimental branch that may end up getting
            deleted.

 You can experiment with changes and then share
            them when they’re something worth sharing or quietly delete them if
            the experiment didn’t work out.

Most branches need to be merged with other branches to keep them
            up-to-date.

When changes happen in different parts of a file, Git can merge
            them automatically.  Sometimes it can’t work out what was supposed to
            happen, so it errs on the side of caution and tells you there’s
            a conflict.

Say you and another developer on your team modify the same line
            of code but in different ways.  Git sees this and can’t programmatically
            determine which one is correct, so it flags them as a conflict
            and waits for you to tell it which change is correct.

            

The alternative that most VCSs and all DVCSs use is called
            optimistic locking

It works like this: Joe and Alice both create clones of the
            repository they share and start making changes.  They both
            make changes to the same file but in different areas of it.
            Alice pushes her change back to their shared repository;
            then Joe attempts to push his.

Joe’s attempt will be rejected, because Git detects that there
            has been a change on the server after he got his copy.  Joe
            has to pull those changes from the repository, handle conflicts
            if there are any, and then push his change back to the server.

 Since it is distributed, there’s
            no central repository to ask what your name or email address is.
            You can tell Git this information by using the
            git config command.

 Your repository in Git is
            stored right alongside your working tree in a directory called
            .git

SHA stands for Secure Hash Algorithm.  It’s an algorithm developed by the 
                U.S. National Security Agency (NSA) to produce shorter strings,
                or message digests, of known data with little possibility
                of a “collision” with another hash.
            

                

Staging a commit prepares it to be committed.  There are three places in
            Git where your code can be stored.  First, the one you work with directly
            when editing files is the working tree.

Second is the index, which I’ll refer to as the staging area.
            The staging area is a buffer
            between your working tree and what is stored in the repository, the third and final area
            in Git

Spend a minute or two with each commit you make, and summarize the changes the same way
                you would as if you were explaining them to another developer sitting next to you.
                A great rule of thumb is to write a simple, one-line sentence that tersely explains
                the commit and then spend another few sentences fully explaining your commit.
            

                

 Two types
            of branches are  useful: different versions of a project
            in different branches and topic branches that deal with a specific
            feature

Git marks a specific point in the history of
            the repository so you can refer to it easily

it takes one parameter: the name of the branch you want to rebase against.

add in a bio link is now placed
            after the final commit in the RB_1.0 branch.

So, how do you handle creating patches to the 1.0.x branch if you don’t
            keep the release branch around?  That’s easy—create a branch off the tag you created.

 You don’t always need to distribute
            the history of your project with your releases.  Often, a tarball or zip
            file of it at the point you tag is enough

 Staged
changes
            are simply changes in your working tree
            that you want to tell your repository about.  When you
            stage a change, it updates what Git refers to as its
            index.  A lot of people, myself included, refer to it
            as the staging area.

The staging area is just that, a place where you can set up
            commits prior to committing to your repository

You can use Git’s interactive add mode to
            select which files or parts of files to stage for a commit.  
            You start it by adding the -i option.

            You can choose which file or files you want to add via 
            patch mode.  Once you make your choice, you are presented with a diff of
            the changed files and given the option to add the changes or not.
            It looks something like this

            A hunk is a change within the file.  Consecutive changes are treated
            as one hunk.  Each different area in a file is treated as its own hunk.

You can name the file anything you want,
                but most people start the file’s name with a period (.) because
                most applications ignore files that begin with a period.

            that your commit message should explain the commit like you would
            to a developer sitting right next to you.

 It won’t add new, untracked files

Git can show you the differences between what’s in your working tree,
                what’s staged and ready to be committed, and what’s in your repository

Calling git diff with no parameters shows you
                the changes in your working tree that you haven’t staged or committed yet.

                View the differences in the staging area and the repository
                by adding --cached to the call:

 You can compare
                everything that’s in your working tree—including your staged changes—against what’s in your repository.
                To do that, execute git diff, and add
                HEAD to the end:

HEAD is a keyword that refers to the most
                recent commit to the branch you’re in

You can move a file in Git by typing 
            git mv <original-file> <new-file>.
            The command tells Git to create new-file with the existing
            file’s content, and it keeps the history and removes 
            original-filename.

git mv is a convenience.  Git can detect the movement of a file, but
            more steps are involved.  You have to move the file and then call
            git add on the new file and
            git rm—the command to remove a file from
            the repository—on the old file.

You can tell your local repository to ignore files like these without sharing the
                exclusion with everyone else.  Edit the file .git/info/exclude,
                and add your rules there.

                    Is this kind of file something that everyone is going to have in their
                    repositories?

                    If the answer to that is yes, you need to ignore it by adding the rule to the
                    .gitignore file and committing that file to the
                    repository.  If it’s only a file you’ll see, add it to your
                    .git/info/exclude file.

 There are three places in
            Git where your code can be stored.  First, the one you work with directly
            when editing files is the working tree.

Second is the index, which I’ll refer to as the staging area.
            The staging area is a buffer
            between your working tree and what is stored in the repository, the third and final area
            in Git

 They allow you to track
            changes with different histories

prompt> git branch -m mymaster master​​




              _NOTE: Rename a branch_

One of the hardest parts of branches is figuring out when to create
            a branch

Experimental changes

New features:

either with the full history or through a squashed
                commit

Bug fixes:

you can create a branch to track your changes
                to that bug

share changes between branches.  This is done through
            merging.

                You can use this when you want to pull the entire history of one
                branch into another

First, you have to start by switching to the branch you
                want to use as your target for the merge.

Now the changes from the alternate branch are
                merged into your master branch.

Squashing  _NOTE: This won’t show as two lines intersecting in a git graph. It just squashes the whole branch commits into one and add to the history of main._

They are “squashed” because Git takes all the history of
                one branch and compresses it into one commit in the other branch

 If the changes
                of a branch represent one individual change, then it’s a
                candidate for squashing.

                Adding the --squash option tells
                git merge to take all the commits from
                the other branch and squash them into one commit:

With the commit name—321d76f—in hand, you
                can cherry-pick it anywhere.  Remember,
                the commit names are universally unique, so your commit name will be
                different from the one I created.  Let’s bring it
                over to the master branch:

The prefix and suffix lines tell you two things.  First, any code that is
            preceded by “<<<<<<<” is
            the code in your current branch, and any code suffixed with “>>>>>>>”
            is from the other branch.

            Once you have saved your changes, you need to stage and commit your 
            changes like normal.

This works only when the branch you’re trying to delete has been
            successfully merged into the current branch you are on.

prompt> git branch -d about​​




 



​​error: The branch 'about' is not an ancestor of your current HEAD.​​




 



​​If you are sure you want to delete it, run 'git branch -D about'.​

You can override this behavior by changing the
            -m option to the -M option.
            The uppercase M tells Git to force an overwrite
            if the other branch exists.  Use this with care.

 Adding the
            -p option tells Git to display the diff
            that revision created.

 You can add
            -1 to the log command to limit the log to
            one commit, -2 to limit it to two
            commits, and so on

You can view the log starting at a given revision by passing the revision as an
            option at the command line:
        



 



​​prompt> git log 7b1558c​​

A caret acts like a minus one.

The tilde and a number operator subtracts N
                from the commit name

All the revision ranges and modifiers are the same as
            git log.  The only difference is that Git
            shows you the changes mashed together instead of incrementally.

Using git diff with tags is a great way to get
            statistics between releases

 git blame
            prefixes every line with the commit name, committer, and timestamp.

 Git
            makes it easy to annotate a portion of a file with its -L
            option.  This tells Git to display only a certain set of line ranges.

One of the values of completely distributed development is that you
                 share only what is ready.

Correcting these small problems with Git is simple.  Make the correction,
            stage the change, and add --amend when
            you commit.

That command introduces a new option to git commit,
            -C.  This option tells Git to use the
            log message from the commit specified—in this case HEAD

Amending a commit should  be done only when you are working with the
            last commit

The simplest way to revert an existing commit is the
            git revert command.  It “reverts” a
            commit by creating a new commit in your repository that reverses
            all the changes made by the original commit.

Normally Git commits the reversal immediately, but you can add the
            -n parameter to tell Git not to
            commit.  This is useful when you need to revert multiple commits.
            Just run multiple git revert commands
            with the -n parameter, and Git
            stages all the changes and waits for you to commit them.

Add --soft when you want to stage all
				the previous commits but not commit them.  This gives you a chance
				to modify the previous commit by adding to or taking away from it.

The final option is --hard, and it should
				be used with care.  It removes the commit from your repository and
				from your working tree.  It’s the equivalent of a delete button on your
				repository with no “undo.”

git rebase in interactive mode is the tool to use to rewrite history

Fetching changes updates your remote branches.  You can see your
            local branches when you run git branch.
            If you add the -r parameter, Git
            shows you the remote branches:

You can check out those branches like a normal branch, but
            you should not change them.  If you want to make a change to them,
            create a local branch from them first, and then make your change.

Running git fetch updates your
            remote branches; it doesn’t merge the changes into your local
            branch.  You can use git pull if you
            want to fetch changes from a remote repository and merge
            them into your local branch at the same time.

 origin is the default
            remote repository name assigned to a repository that you create
            a clone from.

Your default remote repository is
            called origin.  It’s an alias to the
            full name of your repository—whatever you cloned

            To add a new named remote repository, use
            git remote add <name> <repo-url>.
            This command adds Erin’s repository:



 



​​prompt> git remote add erin git://ourcompany.com/dev-erin.git​​




 You can
        quickly find old versions of the software and look through
        the history of a file to figure out how it got to its
        current state.

Mark milestones within your project with tags


Handle release branches to focus development when you’re about to make a release


Group your tags and branches in directory-like structures


Track multiple projects using one or multiple repositories


Use Git’s submodules feature to track external repositories


            Tags act like bookmarks in your repository

The most common use of tags is to mark when the code in your
            project is released

Release branches are a place to prepare code for a release.
            Teams normally use them to segregate code for a release.  What
            segregate means depends on the team

a release branch is created when a project
            is feature complete—that is, it has everything it needs to
            satisfy this release—but hasn’t been fully vetted yet.

This type of branch will have only minimal changes made to it,
            and all will focus around fixes, whether they are bugs or logic,
            but no new features are added.

If each smaller project, or component, is only ever released
                as part of the larger project, then sharing the same history
                might be a good idea.  This makes sure that all the history
                in the repository revolves around one project.

If they are released separately, then they probably need
                their own history

Git stores changes that were made in what it calls deltas.
            git gc compresses those deltas when it
            runs by itself, but it doesn’t recalculate them.  Adding
            --aggressive tells Git to recalculate
            those deltas from scratch when it runs its optimization.