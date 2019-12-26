from report_creator import main
from tools.aws_tools import save_information


@save_information
def handler(event, context):
    return main()
