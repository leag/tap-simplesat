"""Stream type classes for tap-simplesat."""

from __future__ import annotations

import typing as t

from singer_sdk import typing as th  # JSON Schema typing helpers

from tap_simplesat.client import SimplesatStream


class AnswersStream(SimplesatStream):
    name = "answers"
    path = "/answers/search"
    rest_method = "POST"
    records_jsonpath = "$.answers[*]"
    next_page_token_jsonpath = "$.next"
    primary_keys: t.ClassVar[list[str]] = ["id"]
    schema = th.PropertiesList(
        th.Property("id", th.IntegerType, required=True),
        th.Property("choice", th.StringType),
        th.Property("choice_label", th.StringType),
        th.Property("choices", th.StringType),
        th.Property("comment", th.StringType),
        th.Property("follow_up_answer", th.StringType),
        th.Property("follow_up_answer_choice", th.StringType),
        th.Property("follow_up_answer_choices", th.StringType),
        th.Property("published_as_testimonial", th.BooleanType),
        th.Property("created", th.DateTimeType),
        th.Property("modified", th.DateTimeType),
        th.Property(
            "question",
            th.ObjectType(
                th.Property("id", th.IntegerType),
                th.Property("text", th.StringType),
                th.Property("metric", th.StringType),
            ),
        ),
        th.Property("sentiment", th.StringType),
        th.Property(
            "survey",
            th.ObjectType(
                th.Property("id", th.IntegerType),
                th.Property("name", th.StringType),
            ),
        ),
        th.Property("response_id", th.IntegerType),
    ).to_dict()


class QuestionsStream(SimplesatStream):
    name = "questions"
    path = "/questions"
    records_jsonpath = "$.questions[*]"
    primary_keys: t.ClassVar[list[str]] = ["id"]
    schema = th.PropertiesList(
        th.Property("id", th.IntegerType, required=True),
        th.Property(
            "survey",
            th.ObjectType(
                th.Property("id", th.IntegerType),
                th.Property("name", th.StringType),
            ),
        ),
        th.Property("order", th.IntegerType),
        th.Property("metric", th.StringType),
        th.Property("text", th.StringType),
        th.Property("rating_scale", th.BooleanType),
        th.Property("required", th.BooleanType),
        th.Property("choices", th.ArrayType(th.StringType)),
        th.Property(
            "rules",
            th.ArrayType(
                th.ObjectType(
                    th.Property("conditions", th.ArrayType(th.StringType)),
                    th.Property("action", th.StringType),
                    th.Property(
                        "question",
                        th.ObjectType(
                            th.Property("id", th.IntegerType),
                            th.Property("text", th.StringType),
                            th.Property("required", th.BooleanType),
                            th.Property("choices", th.ArrayType(th.StringType)),
                            th.Property("rules", th.ArrayType(th.StringType)),
                        ),
                    ),
                )
            ),
        ),
    ).to_dict()


class ResponsesStream(SimplesatStream):
    name = "responses"
    path = "/responses/search"
    rest_method = "POST"
    records_jsonpath = "$.responses[*]"
    next_page_token_jsonpath = "$.next"
    primary_keys: t.ClassVar[list[str]] = ["id"]
    schema = th.PropertiesList(
        th.Property("id", th.IntegerType, required=True),
        th.Property(
            "survey",
            th.ObjectType(
                th.Property("id", th.IntegerType),
                th.Property("name", th.StringType),
            ),
        ),
        th.Property("tags", th.ArrayType(th.StringType)),
        th.Property("created", th.DateTimeType),
        th.Property("modified", th.DateTimeType),
        th.Property(
            "ticket",
            th.ObjectType(
                th.Property("id", th.IntegerType),
                th.Property("external_id", th.StringType),
                th.Property("subject", th.StringType),
                th.Property(
                    "custom_attributes",
                    th.ObjectType(
                        th.Property("custom_attribute", th.StringType),
                        additional_properties=True,
                    ),
                ),
            ),
        ),
        th.Property(
            "team_members",
            th.ArrayType(
                th.ObjectType(
                    th.Property("email", th.StringType),
                    th.Property("external_id", th.StringType),
                    th.Property("id", th.IntegerType),
                    th.Property("is_primary", th.BooleanType),
                    th.Property("name", th.StringType),
                    th.Property("role", th.StringType),
                )
            ),
        ),
        th.Property(
            "customer",
            th.ObjectType(
                th.Property("id", th.IntegerType),
                th.Property("external_id", th.StringType),
                th.Property("name", th.StringType),
                th.Property("email", th.StringType),
                th.Property("company", th.StringType),
                th.Property("tags", th.ArrayType(th.StringType)),
                th.Property(
                    "custom_attributes",
                    th.ObjectType(
                        th.Property("custom_attribute", th.StringType),
                        additional_properties=True,
                    ),
                ),
            ),
        ),
        th.Property(
            "answers",
            th.ArrayType(
                th.ObjectType(
                    th.Property("id", th.IntegerType),
                    th.Property(
                        "question",
                        th.ObjectType(
                            th.Property("id", th.IntegerType),
                            th.Property("text", th.StringType),
                            th.Property("metric", th.StringType),
                        ),
                    ),
                    th.Property("choice", th.StringType),
                    th.Property("choices", th.StringType),
                    th.Property("comment", th.StringType),
                    th.Property("sentiment", th.StringType),
                    th.Property("follow_up_answer", th.StringType),
                    th.Property("choice_label", th.StringType),
                    th.Property("follow_up_answer_choice", th.StringType),
                    th.Property("follow_up_answer_choices", th.StringType),
                    th.Property(
                        "follow_up_question",
                        th.ObjectType(
                            th.Property("id", th.IntegerType),
                            th.Property("text", th.StringType),
                            th.Property("metric", th.StringType),
                        ),
                    ),
                )
            ),
        ),
    ).to_dict()


class SurveysStream(SimplesatStream):
    name = "surveys"
    path = "/surveys"
    records_jsonpath = "$.surveys[*]"
    primary_keys: t.ClassVar[list[str]] = ["id"]
    schema = th.PropertiesList(
        th.Property("id", th.IntegerType, required=True),
        th.Property("name", th.StringType),
        th.Property("metric", th.StringType),
    ).to_dict()
