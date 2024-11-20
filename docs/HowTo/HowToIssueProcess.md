# How To - Manage Issue Reports

Issue reports are the way to describe a problem we encounter on the FlatSat and associate it with one of the integrated product (eg. Mission SW, GNC SW, Yamcs, etc...).

An issue is a factual observation of what is happening. It is not a description of a task to be done.


## Writing an Issue Report

An issue report shall include at least the following information:

- The version of the item upon which the observation is raised.
- Observations: a factual description of the observed behaviour, and why we think it is not correct. If possible, violated requirements have to be listed.
- Steps to reproduce the problem.
- Steps in the discussion with the provider about the problem (record of exchanges such as mails).
- Priority:

	- High: for blocking problems - issues that, if not solved, prevent us from going any further
	- Low: for things that can remain un-solved for a longer time without impacting our activities, such as documentation problems.
	- Medium: for anything else.

Issues shall show a unique identifier.

Issue reports shall be written in the repository of the integrated items, which are:

- Ymacs: Jaops · Flatsat Development Plan (github.com)
- Asynchronics: Asynchronics · Flatsat Development Plan (github.com)
- Mission SW: 
- GNC SW: 
- ADCS SW:

 
## Weekly Issue follow-up meeting

Every week, a short meeting will go through all the issues to follow the progress of their correction. The current state of progress is logged in the issue itself (with dates). If the issue is verified to be solved, it can be archived.

Each issue has a state, which is represented like this:

- Testers (or anybody) can create an issue -> state shall be **CREATED**.
- The person that is monitoring the provider can inform the provider of the existence of the issue and ask for analysis/correction -> states  changed to **RAISED**.
- The provider provides a solution/correction -> state is changed to **TO_TEST**.

	- If the test is successful, then the issue state can be changed to **CLOSED** by the tester.
	- If the test is unsuccessful, then the issue state is set back to **RAISED**.

- Closed issues can be archived in the weekly meeting only.

In all cases, state changes shall be recorded in the issue  itself.

