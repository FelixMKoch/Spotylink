To sustain a certain scheme to this project this file sould be a guideline to how to contribute. Please stick to these conventions

[TOC]

## Branch-Structure
There are only two fix branches in this project - Development and Master. Usually you also see a QA branch. This one is excluded because it seems irrelevant in the context of this project.  

### Master Branch
You should not directly commit to the master branch - ever. Neither should you merge any branch to this except for the Development branch.  
Merges should only happen in time intervals when every team member reviewed the code and the pipeline does not throw any errors.  

### Development Branch
The Development branch is the source of all new feature branches. If you want to work on one issue, create a new branch with the development branch as a source.  

### New Branch
New branches should look like this:  
Ticket: "Create new branch #42" -> Branch: "#42 - create new branch".  
The branch name must include the number of the issue that is worked on.  

## Commits
Commits should look a certain way. They shall include the commit message as well as the branch number / issue number it is related to.  
For example: Branch: "#42 - create new branch" -> Commit: "#42 created new branch".  

## Merge requests
After a issue is completed the corresponding branch has to be merged into development as soon as possible. A merge request has to be created.  
But the request should not be merged by the person who did all the commits. After the developer creates the merge request, a reviewer should be assigned to have a look at the code and approve the changes. If something went wrong, the reviewer has to report that to the developer - either in the comment section under the merge request or in the comment section of the issue itself. 
Only if the changes are approved, the feature branch may be merged into the Development branch.  

## Review
Commits and branches must be reviewed. The reviewer should do the following steps:
1. Approve that there are no flaws - neither in the code not in the fullfilment of the conventions itself  
1.1. if there are flaws: The reviewer responds in the comment section and the developer has to change the branch until everything is fine
2. If there are no flaws (left) - the reviewer approves the merge request and merges it into the Development branch as soon as possible. 
