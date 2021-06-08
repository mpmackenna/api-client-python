"""
Copyright 2021 Dynatrace LLC

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

from enum import Enum
from requests import Response
from typing import Dict, Any, Optional

from dynatrace.http_client import HttpClient
from dynatrace.dynatrace_object import DynatraceObject
from dynatrace.pagination import PaginatedList


class SloService:
    ENDPOINT = "/api/v2/slo"

    def __init__(self, http_client: HttpClient):
        self.__http_client = http_client

    def list(
        self,
        page_size: Optional[int] = 10,
        time_from: Optional[str] = "now-2w",
        time_to: Optional[str] = None,
        slo_selector: Optional[str] = None,
        sort: Optional[str] = "name",
        time_frame: Optional[str] = "CURRENT",
        page_idx: Optional[int] = 1,
        demo: Optional[bool] = False,
        evaluate: Optional[bool] = False,
    ) -> PaginatedList["Slo"]:
        """Lists all available SLOs along with calculated values

        :param page_size: The amount of SLOs in a single response payload. Max 10,000.
        :param time_from: The start of the requested timeframe.
        :param time_to: The end of the requested timeframe.
        :param slo_selector: The scope of the query. Only SLOs matching the provided criteria are included in the response.
        :param sort: The sorting of SLO entries. Default is by name in ascending order.
        :param time_frame: The timeframe to calculate the SLO values.
        :param page_idx: Only SLOs on the given page are included in the response. The first page has the index '1'.
        :param demo: Get your SLOs (false) or a set of demo SLOs (true)
        :param evaluate: Get your SLOs without them being evaluated (false) or with evaluations (true).

        :returns PaginatedList[Slo]: the list of SLOs matching criteria
        """
        params = {
            "pageSize": page_size,
            "from": time_from,
            "to": time_to,
            "sloSelector": slo_selector,
            "sort": sort,
            "timeFrame": time_frame,
            "pageIdx": page_idx,
            "demo": demo,
            "evaluate": evaluate,
        }
        return PaginatedList(target_class=Slo, http_client=self.__http_client, target_params=params, target_url=f"{self.ENDPOINT}")

    def get(self, slo_id: str, time_from: Optional[str] = "now-2w", time_to: Optional[str] = None) -> "Slo":
        """Gets parameters and the calculated value of an SLO

        :param slo_id: The ID of the required SLO.
        :param time_from: The start of the requested timeframe.
        :param time_to: The end of the requested timeframe.

        :returns Slo: the requested SLO
        """
        params = {
            "from": time_from,
            "to": time_to,
        }
        response = self.__http_client.make_request(path=f"{self.ENDPOINT}/{slo_id}", params=params).json()
        return Slo(raw_element=response)

    def create(
        self,
        name: str,
        target: float,
        warning: float,
        timeframe: str,
        use_rate_metric: Optional[bool] = False,
        metric_rate: Optional[str] = None,
        metric_numerator: Optional[str] = None,
        metric_denominator: Optional[str] = None,
        evaluation_type: Optional[str] = "AGGREGATE",
        entity_filter: Optional[str] = None,
        custom_description: Optional[str] = None,
        enabled: Optional[bool] = False,
    ) -> "Response":
        """Creates a new SLO.

        :param name: The name of the SLO.
        :param target: The target value of the SLO.
        :param warning: The warning value of the SLO. At warning state the SLO is still fulfilled but is getting close to failure.
        :param timeframe: The timeframe for the SLO evaluation. Use the syntax of the global timeframe selector.
        :param use_rate_metric: The type of the metric to use for SLO calculation - an existing percentage-based metric (true) or a ratio of two metrics (false)
        :param metric_rate: The percentage-based metric for the calculation of the SLO. Required when the useRateMetric is set to true.
        :param metric_numerator: The metric for the count of successes (the numerator in rate calculation).Required when the useRateMetric is set to false.
        :param metric_denominator: The total count metric (the denominator in rate calculation). Required when the useRateMetric is set to false.
        :param evaluation_type: The evaluation type of the SLO.
        :param entity_filter: The entity filter for the SLO evaluation. Use the syntax of entity selector.
        :param custom_description: The custom description of the SLO.
        :param enabled: The SLO is enabled (true) or disabled (false).

        :returns Response: HTTP response for the request
        """
        params = {
            "name": name,
            "target": target,
            "warning": warning,
            "timeframe": timeframe,
            "useRateMetric": use_rate_metric,
            "metricRate": metric_rate,
            "metricNumerator": metric_numerator,
            "metricDenominator": metric_denominator,
            "evaluationType": evaluation_type,
            "filter": entity_filter,
            "customDescription": custom_description,
            "enabled": enabled,
        }
        return self.__http_client.make_request(path=self.ENDPOINT, method="POST", params=params)

    def update(
        self,
        slo_id: str,
        name: Optional[str] = None,
        target: Optional[float] = None,
        warning: Optional[float] = None,
        timeframe: Optional[str] = None,
        use_rate_metric: Optional[bool] = None,
        metric_rate: Optional[str] = None,
        metric_numerator: Optional[str] = None,
        metric_denominator: Optional[str] = None,
        evaluation_type: Optional[str] = None,
        entity_filter: Optional[str] = None,
        custom_description: Optional[str] = None,
        enabled: Optional[bool] = None,
    ) -> "Response":
        """Creates a new SLO.

        :param slo_id: The ID of the existing SLO.
        :param name: The name of the SLO.
        :param target: The target value of the SLO.
        :param warning: The warning value of the SLO. At warning state the SLO is still fulfilled but is getting close to failure.
        :param timeframe: The timeframe for the SLO evaluation. Use the syntax of the global timeframe selector.
        :param use_rate_metric: The type of the metric to use for SLO calculation - an existing percentage-based metric (true) or a ratio of two metrics (false)
        :param metric_rate: The percentage-based metric for the calculation of the SLO. Required when the useRateMetric is set to true.
        :param metric_numerator: The metric for the count of successes (the numerator in rate calculation).Required when the useRateMetric is set to false.
        :param metric_denominator: The total count metric (the denominator in rate calculation). Required when the useRateMetric is set to false.
        :param evaluation_type: The evaluation type of the SLO.
        :param entity_filter: The entity filter for the SLO evaluation. Use the syntax of entity selector.
        :param custom_description: The custom description of the SLO.
        :param enabled: The SLO is enabled (true) or disabled (false).

        :returns Response: HTTP response for the request
        """
        params = {
            "name": name,
            "target": target,
            "warning": warning,
            "timeframe": timeframe,
            "useRateMetric": use_rate_metric,
            "metricRate": metric_rate,
            "metricNumerator": metric_numerator,
            "metricDenominator": metric_denominator,
            "evaluationType": evaluation_type,
            "filter": entity_filter,
            "customDescription": custom_description,
            "enabled": enabled,
        }
        return self.__http_client.make_request(path=f"{self.ENDPOINT}/slo/{slo_id}", method="PUT", params=params)

    def delete(self, slo_id: str) -> "Response":
        """Deletes an SLO

        :param slo_id: The ID of the existing SLO.

        :returns Response: HTTP response for the request
        """
        return self.__http_client.make_request(path=f"{self.ENDPOINT}/slo/{slo_id}", method="DELETE")


class Slo(DynatraceObject):
    def _create_from_raw_data(self, raw_element: Dict[str, Any]):
        # required
        self.name: str = raw_element.get("name")
        self.id: str = raw_element.get("id")
        self.target: float = raw_element.get("target")
        self.timeframe: str = raw_element.get("timeframe")
        self.status: SloStatus = SloStatus(raw_element.get("status"))
        self.evaluation_type: SloEvaluationType = SloEvaluationType(raw_element.get("evaluationType"))
        self.use_rate_metric: bool = raw_element.get("useRateMetric")

        # optional
        self.metric_rate: str = raw_element.get("metricRate")
        self.metric_numerator: str = raw_element.get("metricNumerator")
        self.metric_denominator: str = raw_element.get("metricDenominator")
        self.error_budget: Optional[float] = raw_element.get("errorBudget", 0)
        self.numerator_value: Optional[float] = raw_element.get("numeratorValue", 0)
        self.denominator_value: Optional[float] = raw_element.get("denominatorValue", 0)
        self.related_open_problems: Optional[int] = raw_element.get("relatedOpenProblems", 0)
        self.evaluated_percentage: Optional[float] = raw_element.get("evaluatedPercentage", 0)
        self.filter: Optional[str] = raw_element.get("filter")
        self.enabled: Optional[bool] = raw_element.get("enabled", False)
        self.description: Optional[str] = raw_element.get("description")
        self.error: Optional[SloError] = raw_element.get("error", SloError.NONE)


class SloEvaluationType(Enum):
    AGGREGATE = "AGGREGATE"


class SloStatus(Enum):
    FAILURE = "FAILURE"
    SUCCESS = "SUCCESS"
    WARNING = "WARNING"


class SloError(Enum):
    DIFFERENT_ENTITY_TYPE_IN_METRICS = "DIFFERENT_ENTITY_TYPE_IN_METRICS"
    EVALUATION_TIMEFRAME_OUT_OF_BOUNDS = "EVALUATION_TIMEFRAME_OUT_OF_BOUNDS"
    FILTER_MATCHES_IN_CONDITION_LIMIT_EXCEEDED = "FILTER_MATCHES_IN_CONDITION_LIMIT_EXCEEDED"
    INTERNAL_ERROR = "INTERNAL_ERROR"
    INVALID_ENTITY_SELECTOR = "INVALID_ENTITY_SELECTOR"
    INVALID_METRIC_DENOMINATOR = "INVALID_METRIC_DENOMINATOR"
    INVALID_METRIC_NUMERATOR = "INVALID_METRIC_NUMERATOR"
    INVALID_METRIC_SELECTOR = "INVALID_METRIC_SELECTOR"
    INVALID_TIMEFRAME = "INVALID_TIMEFRAME"
    METRICS_NOT_RESOLVED = "METRICS_NOT_RESOLVED"
    METRICS_NO_DATA = "METRICS_NO_DATA"
    METRIC_DENOMINATOR_NOT_RESOLVED = "METRIC_DENOMINATOR_NOT_RESOLVED"
    METRIC_DENOMINATOR_NO_DATA = "METRIC_DENOMINATOR_NO_DATA"
    METRIC_DENOMINATOR_NO_DATA_POINTS = "METRIC_DENOMINATOR_NO_DATA_POINTS"
    METRIC_DENOMINATOR_ZERO = "METRIC_DENOMINATOR_ZERO"
    METRIC_EXPRESSION_NOT_RESOLVED = "METRIC_EXPRESSION_NOT_RESOLVED"
    METRIC_EXPRESSION_NO_DATA = "METRIC_EXPRESSION_NO_DATA"
    METRIC_EXPRESSION_NO_DATA_POINTS = "METRIC_EXPRESSION_NO_DATA_POINTS"
    METRIC_GENERIC_TSM_FAULT = "METRIC_GENERIC_TSM_FAULT"
    METRIC_NUMERATOR_NOT_RESOLVED = "METRIC_NUMERATOR_NOT_RESOLVED"
    METRIC_NUMERATOR_NO_DATA = "METRIC_NUMERATOR_NO_DATA"
    METRIC_NUMERATOR_NO_DATA_POINTS = "METRIC_NUMERATOR_NO_DATA_POINTS"
    METRIC_RATE_NOT_RESOLVED = "METRIC_RATE_NOT_RESOLVED"
    METRIC_RATE_NO_DATA = "METRIC_RATE_NO_DATA"
    METRIC_RATE_NO_DATA_POINTS = "METRIC_RATE_NO_DATA_POINTS"
    METRIC_TOO_MANY_RESULTS = "METRIC_TOO_MANY_RESULTS"
    NONE = "NONE"
