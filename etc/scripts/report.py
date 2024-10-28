import argparse
import os
import subprocess


def get_git_user():
    """Fetches the Git username from global Git configuration."""
    try:
        user_name = subprocess.check_output(["git", "config", "user.name"]).strip().decode("utf-8")
    except subprocess.CalledProcessError:
        user_name = "Unknown User"
    return user_name


def get_git_repos(base_dir, selected_repos=None):
    """Retrieves Git repositories in the specified directory.

    Args:
        base_dir (str): The base directory to search for Git repositories.
        selected_repos (list, optional): Specific repositories to filter by name.

    Returns:
        list: A list of paths to the selected Git repositories.
    """
    repos = []
    for root, dirs, _files in os.walk(base_dir):
        if ".git" in dirs:
            repo_name = os.path.basename(root)
            if selected_repos is None or repo_name in selected_repos:
                repos.append(root)
            dirs.remove(".git")  # Do not traverse into .git folders
    return repos


def get_commits_in_period(repo, start_date, end_date):
    """Fetches commits within a specified date range from a Git repository.

    Args:
        repo (str): The path to the Git repository.
        start_date (str): The start date for the commit log (YYYY-MM-DD).
        end_date (str): The end date for the commit log (YYYY-MM-DD).

    Returns:
        list: A list of commit logs within the specified date range.
    """
    try:
        os.chdir(repo)
        subprocess.check_call(["git", "fetch", "--all"])

        git_log_cmd = [
            "git",
            "log",
            "--all",
            "--since",
            start_date,
            "--until",
            end_date,
            "--pretty=format:%h %ad %s",
            "--date=iso",
        ]
        logs = subprocess.check_output(git_log_cmd).decode("utf-8").splitlines()
        return logs
    except subprocess.CalledProcessError as e:
        print(f"Error fetching commits from {repo}: {e}")
        return []


def generate_report(start_date, end_date, selected_repos=None):
    """Generates a report of Git commits in the specified date range.

    Args:
        start_date (str): Start date for the report (YYYY-MM-DD).
        end_date (str): End date for the report (YYYY-MM-DD).
        selected_repos (list, optional): Specific repositories to include in the report.

    Returns:
        str: A formatted string containing the commit report.
    """
    base_dir = os.path.expanduser("~/Devel")
    git_user = get_git_user()
    repos = get_git_repos(base_dir, selected_repos)

    report = [
        f"Git Commits Report for {git_user}",
        f"Period: {start_date} to {end_date}",
        f"Repositories scanned: {', '.join(os.path.basename(repo) for repo in repos)}",
        "=" * 50,
    ]

    for repo in repos:
        repo_name = os.path.basename(repo)
        commits = get_commits_in_period(repo, start_date, end_date)
        if commits:
            report.append(f"Repository: {repo_name}")
            report.extend(f"  {commit}" for commit in commits)
            report.append("-" * 50)

    return "\n".join(report)


def main():
    """Main function to parse arguments and run the report generation."""
    parser = argparse.ArgumentParser(description="Generate Git commits report.")
    parser.add_argument(
        "-r", "--repos", nargs="+", help="List of repository names to scan (space-separated)."
    )
    parser.add_argument("-s", "--start-date", required=True, help="Start date for commits (YYYY-MM-DD).")
    parser.add_argument("-e", "--end-date", required=True, help="End date for commits (YYYY-MM-DD).")
    args = parser.parse_args()

    report = generate_report(start_date=args.start_date, end_date=args.end_date, selected_repos=args.repos)
    print(report)


if __name__ == "__main__":
    main()
