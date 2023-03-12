from aws_cdk import (
    # Duration,
    Stack, RemovalPolicy,
    aws_dynamodb as dynamodb
    # aws_sqs as sqs,
)

from constructs import Construct


class InfraStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # The code that defines your stack goes here

        self.setup_dynamodb(scope, construct_id, **kwargs)

    def setup_dynamodb(self, scope: Construct, construct_id: str, **kwargs):
        table = dynamodb.Table(
            self,
            "GPTDockUserData",
            partition_key=dynamodb.Attribute(
                name="user_id",
                type=dynamodb.AttributeType.STRING,
            ),
            billing_mode=dynamodb.BillingMode.PAY_PER_REQUEST,
            removal_policy=RemovalPolicy.RETAIN,
            table_name="gpt_dock_user_data",
        )
        dynamodb.Table(
            self,
            "GPTDockClientData",
            partition_key=dynamodb.Attribute(
                name="client_id",
                type=dynamodb.AttributeType.STRING,
            ),
            billing_mode=dynamodb.BillingMode.PAY_PER_REQUEST,
            removal_policy=RemovalPolicy.RETAIN,
            table_name="gpt_dock_client_data",
        )
        # table.add_global_secondary_index(
        #     partition_key=dynamodb.Attribute(
        #         name="tg_id",
        #         type=dynamodb.AttributeType.STRING,
        #     ),
        #     index_name="GPTDockUserDatam_index",
        # )

