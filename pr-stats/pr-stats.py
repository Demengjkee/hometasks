#!/usr/bin/python

import requests
import sys
import argparse
from datetime import datetime
from getpass import getpass


class PRStat:

    def __valid_date(self, s):
        try:
            return datetime.strptime(s, "%Y-%m-%d")
        except ValueError:
            msg = "Not a valid date: '{0}'.".format(s)
            raise argparse.ArgumentTypeError(msg)

    def __init__(self):

        parser = argparse.ArgumentParser(
            description='GitHub PR statistics utill.',
            usage="pr-stats.py [-h] [-v] [OPTIONS] " +
                  "[-(d|D) YYYY-MM-DD] <user> <repo>"
        )

        parser.add_argument(
            "-v", "--version", action='version',
            version='pr-stats v0.1 alpha',
            help="Print version"
        )

        parser.add_argument(
            "-o", "--days-opened",
            action="store_true",
            help="Print number of days PRs were open"
        )
        parser.add_argument(
            "-r", "--ratio",
            action="store_true",
            help="Print merged/closed ratio"
        )
        parser.add_argument(
            "-c", "--comments-number",
            action="store_true",
            help="Print number of comments"
        )
        parser.add_argument(
            "--day-of-week-opened",
            action="store_true",
            help="Show days of week when PRs were opened"
        )
        parser.add_argument(
            "--day-of-week-closed",
            action="store_true",
            help="Show days of week when PRs were closed"
        )
        parser.add_argument(
            "--hour-opened",
            action="store_true",
            help="Show hours of the day when PRs were opened"
        )
        parser.add_argument(
            "--hour-closed",
            action="store_true",
            help="Show hours of the day when PRs were closed"
        )
        parser.add_argument(
            "--week-opened",
            action="store_true",
            help="Show week when PRs were opened"
        )
        parser.add_argument(
            "--week-closed",
            action="store_true",
            help="Show week when PRs were closed"
        )
        parser.add_argument(
            "-u", "--user-opened",
            action="store_true",
            help="Print users who opened PRs"
        )
        parser.add_argument(
            "-U", "--user-closed",
            action="store_true",
            help="Print users who closed PRs"
        )
        parser.add_argument(
            "--labels",
            action="store_true",
            help="Print labels associated with PRs"
        )
        parser.add_argument(
            "-l", "--lines-added",
            action="store_true",
            help="Print number of lines added"
        )
        parser.add_argument(
            "-L", "--lines-deleted",
            action="store_true",
            help="Print number of lines deleted"
        )

        parser.add_argument(
            "-d", "--opened-before",
            type=self.__valid_date,
            help="Print PRs opened only BEFORE specified date"
        )
        parser.add_argument(
            "-D", "--opened-after",
            type=self.__valid_date,
            help="Print PRs opened only AFTER specified date"
        )

        parser.add_argument(
            "user",
            metavar="user",
            type=str, nargs=1,
            help='GitHub repo owner'
        )
        parser.add_argument(
            "repo",
            metavar="repo",
            type=str, nargs=1,
            help='GitHub repo name'
        )

        self.__args = parser.parse_args(sys.argv[1:])
        print(self.__args)
        self.__get_auth()

    def __get_auth(self):
        self.__username = input("Username: ")
        self.__password = getpass("Password for %s: " % self.__username)

    def __generate_request(self):
        base_url = "https://api.github.com/repos/"
        self.__url = base_url + self.__args.user[0] + \
            "/" + self.__args.repo[0] + "/pulls?state=all"
        return self.__url

    def __get_stat(self, url):
        resp = requests.get(
            url,
            auth=(self.__username, self.__password)
        )
        if resp.status_code != 200:
            raise requests.RequestException(response=resp)
        else:
            return resp.json()

    def __check_date(self, date):
        if self.__args.opened_before is None:
            self.__args.opened_before = datetime.max
        if self.__args.opened_after is None:
            self.__args.opened_after = datetime.min
        return True \
            if date > self.__args.opened_after \
            and date < self.__args.opened_before \
            else False

    def __calculate_ratio(self, data):
        status_list = [pr['state'] for pr in data]
        closed = status_list.count("closed")
        merged = status_list.count("merged")
        try:
            ratio = merged / closed
        except ZeroDivisionError:
            ratio = "No Closed PRs and no Merged"
        return ratio

    def parse_stat(self):
        stat = self.__get_stat(self.__generate_request())
        print("------------------------------------------------")
        try:
            for pr in stat:
                if self.__check_date(
                        datetime.strptime(
                            pr['created_at'].split("T")[0],
                            '%Y-%m-%d'
                        )):
                    print("PR id:" + str(pr['number']) +
                          " Name: " + pr["title"])
                    if self.__args.days_opened:
                        print("Opened " + str(
                            datetime.now() -
                            datetime.strptime(
                                pr['created_at'].split("T")[0],
                                '%Y-%m-%d')
                            ) +
                            " ago"
                        )
                    if self.__args.comments_number:
                        comments = self.__get_stat(pr['comments_url'])
                        print("Comment number: " + str(len(comments)))
                    if self.__args.user_opened:
                        print("Opened by: " + pr['user']['login'])
                    if self.__args.user_closed:
                        print("Closed by:")
                    if self.__args.labels:
                        print("Labels:")
                    if self.__args.lines_added:
                        print("Lines added: ")
                    if self.__args.lines_deleted:
                        print("Lines deleted: ")
                    if self.__args.day_of_week_closed:
                        if pr['closed_at'] != 'null':
                            print("Day of week closed: " + str(
                                datetime.strptime(
                                    pr['closed_at'].split("T")[0],
                                    '%Y-%m-%d').weekday()
                                )
                            )
                    if self.__args.day_of_week_opened:
                        print("Day of week created: " + str(
                            datetime.strptime(
                                pr['created_at'].split("T")[0],
                                '%Y-%m-%d').weekday()
                            )
                        )
                    if self.__args.hour_opened:
                        print("Hour opened: " + str(
                            datetime.strptime(
                                pr['created_at'].split("T")[1].split("Z")[0],
                                '%H:%M:%S').hour
                            )
                        )
                    if self.__args.hour_closed:
                        if pr['closed_at'] != 'null':
                            print("Hour closed: " + str(
                                datetime.strptime(
                                   pr['closed_at'].split("T")[1].split("Z")[0],
                                   '%H:%M:%S').hour
                                )
                            )
                    if self.__args.week_opened:
                        print("Week opened: " + str(
                            datetime.strptime(
                                pr['created_at'].split("T")[0],
                                '%Y-%m-%d').isocalendar()[1]
                            )
                        )
                    if self.__args.week_closed:
                        if pr['closed_at'] != 'null':
                            print("Week closed: " + str(
                                datetime.strptime(
                                    pr['closed_at'].split("T")[0],
                                    '%Y-%m-%d').isocalendar()[1]
                                )
                            )
                    print("------------------------------------------------")
        except KeyboardInterrupt:
            print("Interrupted")
        if self.__args.ratio:
            print("Merged/Closed ratio: " + str(self.__calculate_ratio(stat)))

if __name__ == "__main__":
    tmp = PRStat()
    try:
        tmp.parse_stat()
    except requests.RequestException as e:
        print(e.response.status_code)
        print(e.response.json()['message'])
