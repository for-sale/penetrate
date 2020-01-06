
class IssueType:
    issue_type_id = {
        "TouchScreen&Firmware触屏及固件": 1,
        "Servo Cable for lifting system wrong/loose伺服线缆错误/松脱-双头切换系统": 2,
        "Touch Fail触控失效": 3
    }

    def type_to_id(self, issue_type):
        issue_id = list()
        for key in issue_type:
            if key in self.issue_type_id:
                issue_id.append(self.issue_type_id[key])
        return sorted(issue_id)


def type_to_id(issue_type):
    issuetype = IssueType()
    return issuetype.type_to_id(issue_type)

