#!/usr/local/bin/python
from makeBuild import import_settings

def main():
    """Writes the qc yaml for GH actions passing the loads from enanomapper.yaml"""
    config = import_settings("enanomapper.yaml")
    robot = config["robot-commands"]["robot"]
    robot_jar = config["robot-commands"]["robot-jar"]
    merge = config["robot-commands"]["merge"]
    verify = config["robot-commands"]["verify"]
    report = config["robot-commands"]["report"]
    validate = config["robot-commands"]["validate-profile"]
    odk_dashboard = config["odk-dashboard"]
    dispatch = config["robot-commands"]["dispatch"]
    commit_message = config["robot-commands"]["commit-message"]
    added_merged = ""
    with open("../../../.github/workflows/qc.yml", "a+") as qc_yaml:
        qc_yaml.truncate(0)
        qc_yaml.write("""name: workflow qc eNanoMapper
on:
    {}
jobs:
    qc:
        runs-on: ubuntu-latest
        steps:
        - name: checkout repo
          uses: actions/checkout@v2
        - name: get robot
          run: |
            ls
            wget {}
            wget {}
            chmod 777 robo*
    """.format(dispatch, robot, robot_jar))
        if merge == True:
            qc_yaml.write("""
        - name: merge
          run: sh robot merge -i enanomapper.owl -o enanomapper-full.owl""")
            added_merged = "git add enanomapper-full.owl"
        if verify == True:
            pass
        if report == True:
            qc_yaml.write("""
        - name: report
          run: sh robot report --fail-on none -i enanomapper.owl -o robot-report/report.tsv""")
            added_report = "git add ./robot-report/*"
        if validate == True:
            pass # to be added
        if odk_dashboard == True:
            pass # to be added
        qc_yaml.write("""
  # Commit and push
        - name: Commit OWL files
          run: |
            {}
            {}
            git config --local user.email "action@github.com"
            git config --local user.name "GitHub Action"
            git commit -m "{}" ./robot-report/* enanomapper-full.owl
        - name: Push changes
          uses: ad-m/github-push-action@master
          with:
            github_token: ${{ secrets.GITHUB_TOKEN }}
            branch: master   
  """.format(added_merged, added_report, commit_message))

if __name__ == "__main__":
    main()