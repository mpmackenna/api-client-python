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

from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import List, Dict, Any, Optional, Union
from dynatrace import http_client

from requests import Response

from dynatrace.environment_v2.schemas import ConfigurationMetadata
from dynatrace.dynatrace_object import DynatraceObject
from dynatrace.environment_v2.monitored_entities import EntityShortRepresentation
from dynatrace.http_client import HttpClient
from dynatrace.pagination import PaginatedList


class ManagementZoneService:
    ENDPOINT = "/api/config/v1/managementZones"

    def __init__(self, http_client: HttpClient):
        self.__http_client = http_client

    def list(self, page_size: int = 200) -> PaginatedList["ManagementZoneShortRepresentation"]:
        """
        List all management zones.

        :param page_size: The number of results per result page. Must be between 1 and 500
            Default value : 200
        """
        params = {"pageSize": page_size}
        return PaginatedList(ManagementZoneShortRepresentation, self.__http_client, f"{self.ENDPOINT}", params, list_item="values")

    def get(self, management_zone_id: str) -> "ManagementZone":
        """Gets the description of a management zone referenced by ID.

        :param _id: The ID of the required management zone.

        :returns Event: the requested management zone
        """
        response = self.__http_client.make_request(path=f"{self.ENDPOINT}/{management_zone_id}")
        return ManagementZone(raw_element=response.json(), http_client=self.__http_client)

    def delete(self, management_zone_id: str):
        """Deletes the specified management zone

        :param networkzone_id: the ID of the management zone
        :return: HTTP response
        """
        return self.__http_client.make_request(path=f"{self.ENDPOINT}/{management_zone_id}", method="DELETE")


class PropagationType(Enum):
    SERVICE_TO_PROCESS_GROUP_LIKE = "SERVICE_TO_PROCESS_GROUP_LIKE"
    SERVICE_TO_HOST_LIKE = "SERVICE_TO_HOST_LIKE"
    PROCESS_GROUP_TO_HOST = "PROCESS_GROUP_TO_HOST"
    PROCESS_GROUP_TO_SERVICE = "PROCESS_GROUP_TO_SERVICE"
    HOST_TO_PROCESS_GROUP_INSTANCE = "HOST_TO_PROCESS_GROUP_INSTANCE"
    AZURE_TO_PG = "AZURE_TO_PG"
    AZURE_TO_SERVICE = "AZURE_TO_SERVICE"
    NONE = None


class ConditionKeyAttribute(Enum):
    APPMON_SERVER_NAME = "APPMON_SERVER_NAME"
    APPMON_SYSTEM_PROFILE_NAME = "APPMON_SYSTEM_PROFILE_NAME"
    AWS_ACCOUNT_ID = "AWS_ACCOUNT_ID"
    AWS_ACCOUNT_NAME = "AWS_ACCOUNT_NAME"
    AWS_APPLICATION_LOAD_BALANCER_NAME = "AWS_APPLICATION_LOAD_BALANCER_NAME"
    AWS_APPLICATION_LOAD_BALANCER_TAGS = "AWS_APPLICATION_LOAD_BALANCER_TAGS"
    AWS_AUTO_SCALING_GROUP_NAME = "AWS_AUTO_SCALING_GROUP_NAME"
    AWS_AUTO_SCALING_GROUP_TAGS = "AWS_AUTO_SCALING_GROUP_TAGS"
    AWS_AVAILABILITY_ZONE_NAME = "AWS_AVAILABILITY_ZONE_NAME"
    AWS_CLASSIC_LOAD_BALANCER_FRONTEND_PORTS = "AWS_CLASSIC_LOAD_BALANCER_FRONTEND_PORTS"
    AWS_CLASSIC_LOAD_BALANCER_NAME = "AWS_CLASSIC_LOAD_BALANCER_NAME"
    AWS_CLASSIC_LOAD_BALANCER_TAGS = "AWS_CLASSIC_LOAD_BALANCER_TAGS"
    AWS_NETWORK_LOAD_BALANCER_NAME = "AWS_NETWORK_LOAD_BALANCER_NAME"
    AWS_NETWORK_LOAD_BALANCER_TAGS = "AWS_NETWORK_LOAD_BALANCER_TAGS"
    AWS_RELATIONAL_DATABASE_SERVICE_DB_NAME = "AWS_RELATIONAL_DATABASE_SERVICE_DB_NAME"
    AWS_RELATIONAL_DATABASE_SERVICE_ENDPOINT = "AWS_RELATIONAL_DATABASE_SERVICE_ENDPOINT"
    AWS_RELATIONAL_DATABASE_SERVICE_ENGINE = "AWS_RELATIONAL_DATABASE_SERVICE_ENGINE"
    AWS_RELATIONAL_DATABASE_SERVICE_INSTANCE_CLASS = "AWS_RELATIONAL_DATABASE_SERVICE_INSTANCE_CLASS"
    AWS_RELATIONAL_DATABASE_SERVICE_NAME = "AWS_RELATIONAL_DATABASE_SERVICE_NAME"
    AWS_RELATIONAL_DATABASE_SERVICE_PORT = "AWS_RELATIONAL_DATABASE_SERVICE_PORT"
    AWS_RELATIONAL_DATABASE_SERVICE_TAGS = "AWS_RELATIONAL_DATABASE_SERVICE_TAGS"
    AZURE_ENTITY_NAME = "AZURE_ENTITY_NAME"
    AZURE_ENTITY_TAGS = "AZURE_ENTITY_TAGS"
    AZURE_MGMT_GROUP_NAME = "AZURE_MGMT_GROUP_NAME"
    AZURE_MGMT_GROUP_UUID = "AZURE_MGMT_GROUP_UUID"
    AZURE_REGION_NAME = "AZURE_REGION_NAME"
    AZURE_SCALE_SET_NAME = "AZURE_SCALE_SET_NAME"
    AZURE_SUBSCRIPTION_NAME = "AZURE_SUBSCRIPTION_NAME"
    AZURE_SUBSCRIPTION_UUID = "AZURE_SUBSCRIPTION_UUID"
    AZURE_TENANT_NAME = "AZURE_TENANT_NAME"
    AZURE_TENANT_UUID = "AZURE_TENANT_UUID"
    AZURE_VM_NAME = "AZURE_VM_NAME"
    BROWSER_MONITOR_NAME = "BROWSER_MONITOR_NAME"
    BROWSER_MONITOR_TAGS = "BROWSER_MONITOR_TAGS"
    CLOUD_APPLICATION_LABELS = "CLOUD_APPLICATION_LABELS"
    CLOUD_APPLICATION_NAME = "CLOUD_APPLICATION_NAME"
    CLOUD_APPLICATION_NAMESPACE_LABELS = "CLOUD_APPLICATION_NAMESPACE_LABELS"
    CLOUD_APPLICATION_NAMESPACE_NAME = "CLOUD_APPLICATION_NAMESPACE_NAME"
    CLOUD_FOUNDRY_FOUNDATION_NAME = "CLOUD_FOUNDRY_FOUNDATION_NAME"
    CLOUD_FOUNDRY_ORG_NAME = "CLOUD_FOUNDRY_ORG_NAME"
    CUSTOM_APPLICATION_NAME = "CUSTOM_APPLICATION_NAME"
    CUSTOM_APPLICATION_PLATFORM = "CUSTOM_APPLICATION_PLATFORM"
    CUSTOM_APPLICATION_TAGS = "CUSTOM_APPLICATION_TAGS"
    CUSTOM_APPLICATION_TYPE = "CUSTOM_APPLICATION_TYPE"
    CUSTOM_DEVICE_DETECTED_NAME = "CUSTOM_DEVICE_DETECTED_NAME"
    CUSTOM_DEVICE_DNS_ADDRESS = "CUSTOM_DEVICE_DNS_ADDRESS"
    CUSTOM_DEVICE_GROUP_NAME = "CUSTOM_DEVICE_GROUP_NAME"
    CUSTOM_DEVICE_GROUP_TAGS = "CUSTOM_DEVICE_GROUP_TAGS"
    CUSTOM_DEVICE_IP_ADDRESS = "CUSTOM_DEVICE_IP_ADDRESS"
    CUSTOM_DEVICE_METADATA = "CUSTOM_DEVICE_METADATA"
    CUSTOM_DEVICE_NAME = "CUSTOM_DEVICE_NAME"
    CUSTOM_DEVICE_PORT = "CUSTOM_DEVICE_PORT"
    CUSTOM_DEVICE_TAGS = "CUSTOM_DEVICE_TAGS"
    CUSTOM_DEVICE_TECHNOLOGY = "CUSTOM_DEVICE_TECHNOLOGY"
    DATA_CENTER_SERVICE_DECODER_TYPE = "DATA_CENTER_SERVICE_DECODER_TYPE"
    DATA_CENTER_SERVICE_IP_ADDRESS = "DATA_CENTER_SERVICE_IP_ADDRESS"
    DATA_CENTER_SERVICE_METADATA = "DATA_CENTER_SERVICE_METADATA"
    DATA_CENTER_SERVICE_NAME = "DATA_CENTER_SERVICE_NAME"
    DATA_CENTER_SERVICE_PORT = "DATA_CENTER_SERVICE_PORT"
    DATA_CENTER_SERVICE_TAGS = "DATA_CENTER_SERVICE_TAGS"
    DOCKER_CONTAINER_NAME = "DOCKER_CONTAINER_NAME"
    DOCKER_FULL_IMAGE_NAME = "DOCKER_FULL_IMAGE_NAME"
    DOCKER_IMAGE_VERSION = "DOCKER_IMAGE_VERSION"
    DOCKER_STRIPPED_IMAGE_NAME = "DOCKER_STRIPPED_IMAGE_NAME"
    EC2_INSTANCE_AMI_ID = "EC2_INSTANCE_AMI_ID"
    EC2_INSTANCE_AWS_INSTANCE_TYPE = "EC2_INSTANCE_AWS_INSTANCE_TYPE"
    EC2_INSTANCE_AWS_SECURITY_GROUP = "EC2_INSTANCE_AWS_SECURITY_GROUP"
    EC2_INSTANCE_BEANSTALK_ENV_NAME = "EC2_INSTANCE_BEANSTALK_ENV_NAME"
    EC2_INSTANCE_ID = "EC2_INSTANCE_ID"
    EC2_INSTANCE_NAME = "EC2_INSTANCE_NAME"
    EC2_INSTANCE_PRIVATE_HOST_NAME = "EC2_INSTANCE_PRIVATE_HOST_NAME"
    EC2_INSTANCE_PUBLIC_HOST_NAME = "EC2_INSTANCE_PUBLIC_HOST_NAME"
    EC2_INSTANCE_TAGS = "EC2_INSTANCE_TAGS"
    ENTERPRISE_APPLICATION_DECODER_TYPE = "ENTERPRISE_APPLICATION_DECODER_TYPE"
    ENTERPRISE_APPLICATION_IP_ADDRESS = "ENTERPRISE_APPLICATION_IP_ADDRESS"
    ENTERPRISE_APPLICATION_METADATA = "ENTERPRISE_APPLICATION_METADATA"
    ENTERPRISE_APPLICATION_NAME = "ENTERPRISE_APPLICATION_NAME"
    ENTERPRISE_APPLICATION_PORT = "ENTERPRISE_APPLICATION_PORT"
    ENTERPRISE_APPLICATION_TAGS = "ENTERPRISE_APPLICATION_TAGS"
    ESXI_HOST_CLUSTER_NAME = "ESXI_HOST_CLUSTER_NAME"
    ESXI_HOST_HARDWARE_MODEL = "ESXI_HOST_HARDWARE_MODEL"
    ESXI_HOST_HARDWARE_VENDOR = "ESXI_HOST_HARDWARE_VENDOR"
    ESXI_HOST_NAME = "ESXI_HOST_NAME"
    ESXI_HOST_PRODUCT_NAME = "ESXI_HOST_PRODUCT_NAME"
    ESXI_HOST_PRODUCT_VERSION = "ESXI_HOST_PRODUCT_VERSION"
    ESXI_HOST_TAGS = "ESXI_HOST_TAGS"
    EXTERNAL_MONITOR_ENGINE_DESCRIPTION = "EXTERNAL_MONITOR_ENGINE_DESCRIPTION"
    EXTERNAL_MONITOR_ENGINE_NAME = "EXTERNAL_MONITOR_ENGINE_NAME"
    EXTERNAL_MONITOR_ENGINE_TYPE = "EXTERNAL_MONITOR_ENGINE_TYPE"
    EXTERNAL_MONITOR_NAME = "EXTERNAL_MONITOR_NAME"
    EXTERNAL_MONITOR_TAGS = "EXTERNAL_MONITOR_TAGS"
    GEOLOCATION_SITE_NAME = "GEOLOCATION_SITE_NAME"
    GOOGLE_CLOUD_PLATFORM_ZONE_NAME = "GOOGLE_CLOUD_PLATFORM_ZONE_NAME"
    GOOGLE_COMPUTE_INSTANCE_ID = "GOOGLE_COMPUTE_INSTANCE_ID"
    GOOGLE_COMPUTE_INSTANCE_MACHINE_TYPE = "GOOGLE_COMPUTE_INSTANCE_MACHINE_TYPE"
    GOOGLE_COMPUTE_INSTANCE_NAME = "GOOGLE_COMPUTE_INSTANCE_NAME"
    GOOGLE_COMPUTE_INSTANCE_PROJECT = "GOOGLE_COMPUTE_INSTANCE_PROJECT"
    GOOGLE_COMPUTE_INSTANCE_PROJECT_ID = "GOOGLE_COMPUTE_INSTANCE_PROJECT_ID"
    GOOGLE_COMPUTE_INSTANCE_PUBLIC_IP_ADDRESSES = "GOOGLE_COMPUTE_INSTANCE_PUBLIC_IP_ADDRESSES"
    HOST_AIX_LOGICAL_CPU_COUNT = "HOST_AIX_LOGICAL_CPU_COUNT"
    HOST_AIX_SIMULTANEOUS_THREADS = "HOST_AIX_SIMULTANEOUS_THREADS"
    HOST_AIX_VIRTUAL_CPU_COUNT = "HOST_AIX_VIRTUAL_CPU_COUNT"
    HOST_ARCHITECTURE = "HOST_ARCHITECTURE"
    HOST_AWS_NAME_TAG = "HOST_AWS_NAME_TAG"
    HOST_AZURE_COMPUTE_MODE = "HOST_AZURE_COMPUTE_MODE"
    HOST_AZURE_SKU = "HOST_AZURE_SKU"
    HOST_AZURE_WEB_APPLICATION_HOST_NAMES = "HOST_AZURE_WEB_APPLICATION_HOST_NAMES"
    HOST_AZURE_WEB_APPLICATION_SITE_NAMES = "HOST_AZURE_WEB_APPLICATION_SITE_NAMES"
    HOST_BITNESS = "HOST_BITNESS"
    HOST_BOSH_AVAILABILITY_ZONE = "HOST_BOSH_AVAILABILITY_ZONE"
    HOST_BOSH_DEPLOYMENT_ID = "HOST_BOSH_DEPLOYMENT_ID"
    HOST_BOSH_INSTANCE_ID = "HOST_BOSH_INSTANCE_ID"
    HOST_BOSH_INSTANCE_NAME = "HOST_BOSH_INSTANCE_NAME"
    HOST_BOSH_NAME = "HOST_BOSH_NAME"
    HOST_BOSH_STEMCELL_VERSION = "HOST_BOSH_STEMCELL_VERSION"
    HOST_CLOUD_TYPE = "HOST_CLOUD_TYPE"
    HOST_CPU_CORES = "HOST_CPU_CORES"
    HOST_CUSTOM_METADATA = "HOST_CUSTOM_METADATA"
    HOST_DETECTED_NAME = "HOST_DETECTED_NAME"
    HOST_GROUP_ID = "HOST_GROUP_ID"
    HOST_GROUP_NAME = "HOST_GROUP_NAME"
    HOST_HYPERVISOR_TYPE = "HOST_HYPERVISOR_TYPE"
    HOST_IP_ADDRESS = "HOST_IP_ADDRESS"
    HOST_KUBERNETES_LABELS = "HOST_KUBERNETES_LABELS"
    HOST_LOGICAL_CPU_CORES = "HOST_LOGICAL_CPU_CORES"
    HOST_NAME = "HOST_NAME"
    HOST_ONEAGENT_CUSTOM_HOST_NAME = "HOST_ONEAGENT_CUSTOM_HOST_NAME"
    HOST_OS_TYPE = "HOST_OS_TYPE"
    HOST_OS_VERSION = "HOST_OS_VERSION"
    HOST_PAAS_MEMORY_LIMIT = "HOST_PAAS_MEMORY_LIMIT"
    HOST_PAAS_TYPE = "HOST_PAAS_TYPE"
    HOST_TAGS = "HOST_TAGS"
    HOST_TECHNOLOGY = "HOST_TECHNOLOGY"
    HTTP_MONITOR_NAME = "HTTP_MONITOR_NAME"
    HTTP_MONITOR_TAGS = "HTTP_MONITOR_TAGS"
    KUBERNETES_CLUSTER_NAME = "KUBERNETES_CLUSTER_NAME"
    KUBERNETES_NODE_NAME = "KUBERNETES_NODE_NAME"
    MOBILE_APPLICATION_NAME = "MOBILE_APPLICATION_NAME"
    MOBILE_APPLICATION_PLATFORM = "MOBILE_APPLICATION_PLATFORM"
    MOBILE_APPLICATION_TAGS = "MOBILE_APPLICATION_TAGS"
    NAME_OF_COMPUTE_NODE = "NAME_OF_COMPUTE_NODE"
    OPENSTACK_ACCOUNT_NAME = "OPENSTACK_ACCOUNT_NAME"
    OPENSTACK_ACCOUNT_PROJECT_NAME = "OPENSTACK_ACCOUNT_PROJECT_NAME"
    OPENSTACK_AVAILABILITY_ZONE_NAME = "OPENSTACK_AVAILABILITY_ZONE_NAME"
    OPENSTACK_PROJECT_NAME = "OPENSTACK_PROJECT_NAME"
    OPENSTACK_REGION_NAME = "OPENSTACK_REGION_NAME"
    OPENSTACK_VM_INSTANCE_TYPE = "OPENSTACK_VM_INSTANCE_TYPE"
    OPENSTACK_VM_NAME = "OPENSTACK_VM_NAME"
    OPENSTACK_VM_SECURITY_GROUP = "OPENSTACK_VM_SECURITY_GROUP"
    PROCESS_GROUP_AZURE_HOST_NAME = "PROCESS_GROUP_AZURE_HOST_NAME"
    PROCESS_GROUP_AZURE_SITE_NAME = "PROCESS_GROUP_AZURE_SITE_NAME"
    PROCESS_GROUP_CUSTOM_METADATA = "PROCESS_GROUP_CUSTOM_METADATA"
    PROCESS_GROUP_DETECTED_NAME = "PROCESS_GROUP_DETECTED_NAME"
    PROCESS_GROUP_ID = "PROCESS_GROUP_ID"
    PROCESS_GROUP_LISTEN_PORT = "PROCESS_GROUP_LISTEN_PORT"
    PROCESS_GROUP_NAME = "PROCESS_GROUP_NAME"
    PROCESS_GROUP_PREDEFINED_METADATA = "PROCESS_GROUP_PREDEFINED_METADATA"
    PROCESS_GROUP_TAGS = "PROCESS_GROUP_TAGS"
    PROCESS_GROUP_TECHNOLOGY = "PROCESS_GROUP_TECHNOLOGY"
    PROCESS_GROUP_TECHNOLOGY_EDITION = "PROCESS_GROUP_TECHNOLOGY_EDITION"
    PROCESS_GROUP_TECHNOLOGY_VERSION = "PROCESS_GROUP_TECHNOLOGY_VERSION"
    SERVICE_AKKA_ACTOR_SYSTEM = "SERVICE_AKKA_ACTOR_SYSTEM"
    SERVICE_CTG_SERVICE_NAME = "SERVICE_CTG_SERVICE_NAME"
    SERVICE_DATABASE_HOST_NAME = "SERVICE_DATABASE_HOST_NAME"
    SERVICE_DATABASE_NAME = "SERVICE_DATABASE_NAME"
    SERVICE_DATABASE_TOPOLOGY = "SERVICE_DATABASE_TOPOLOGY"
    SERVICE_DATABASE_VENDOR = "SERVICE_DATABASE_VENDOR"
    SERVICE_DETECTED_NAME = "SERVICE_DETECTED_NAME"
    SERVICE_ESB_APPLICATION_NAME = "SERVICE_ESB_APPLICATION_NAME"
    SERVICE_IBM_CTG_GATEWAY_URL = "SERVICE_IBM_CTG_GATEWAY_URL"
    SERVICE_IIB_APPLICATION_NAME = "SERVICE_IIB_APPLICATION_NAME"
    SERVICE_MESSAGING_LISTENER_CLASS_NAME = "SERVICE_MESSAGING_LISTENER_CLASS_NAME"
    SERVICE_NAME = "SERVICE_NAME"
    SERVICE_PORT = "SERVICE_PORT"
    SERVICE_PUBLIC_DOMAIN_NAME = "SERVICE_PUBLIC_DOMAIN_NAME"
    SERVICE_REMOTE_ENDPOINT = "SERVICE_REMOTE_ENDPOINT"
    SERVICE_REMOTE_SERVICE_NAME = "SERVICE_REMOTE_SERVICE_NAME"
    SERVICE_TAGS = "SERVICE_TAGS"
    SERVICE_TECHNOLOGY = "SERVICE_TECHNOLOGY"
    SERVICE_TECHNOLOGY_EDITION = "SERVICE_TECHNOLOGY_EDITION"
    SERVICE_TECHNOLOGY_VERSION = "SERVICE_TECHNOLOGY_VERSION"
    SERVICE_TOPOLOGY = "SERVICE_TOPOLOGY"
    SERVICE_TYPE = "SERVICE_TYPE"
    SERVICE_WEB_APPLICATION_ID = "SERVICE_WEB_APPLICATION_ID"
    SERVICE_WEB_CONTEXT_ROOT = "SERVICE_WEB_CONTEXT_ROOT"
    SERVICE_WEB_SERVER_ENDPOINT = "SERVICE_WEB_SERVER_ENDPOINT"
    SERVICE_WEB_SERVER_NAME = "SERVICE_WEB_SERVER_NAME"
    SERVICE_WEB_SERVICE_NAME = "SERVICE_WEB_SERVICE_NAME"
    SERVICE_WEB_SERVICE_NAMESPACE = "SERVICE_WEB_SERVICE_NAMESPACE"
    VMWARE_DATACENTER_NAME = "VMWARE_DATACENTER_NAME"
    VMWARE_VM_NAME = "VMWARE_VM_NAME"
    WEB_APPLICATION_NAME = "WEB_APPLICATION_NAME"
    WEB_APPLICATION_NAME_PATTERN = "WEB_APPLICATION_NAME_PATTERN"
    WEB_APPLICATION_TAGS = "WEB_APPLICATION_TAGS"
    WEB_APPLICATION_TYPE = "WEB_APPLICATION_TYPE"
    NONE = None


class ConditionKeyType(Enum):
    PROCESS_CUSTOM_METADATA_KEY = "PROCESS_CUSTOM_METADATA_KEY"
    HOST_CUSTOM_METADATA_KEY = "HOST_CUSTOM_METADATA_KEY"
    PROCESS_PREDEFINED_METADATA_KEY = "PROCESS_PREDEFINED_METADATA_KEY"
    STRING = "STRING"
    STATIC = "STATIC"
    NONE = None


class ComparisonBasicType(Enum):
    APPLICATION_TYPE = "APPLICATION_TYPE"
    AZURE_COMPUTE_MODE = "AZURE_COMPUTE_MODE"
    AZURE_SKU = "AZURE_SKU"
    BITNESS = "BITNESS"
    CLOUD_TYPE = "CLOUD_TYPE"
    CUSTOM_APPLICATION_TYPE = "CUSTOM_APPLICATION_TYPE"
    DATABASE_TOPOLOGY = "DATABASE_TOPOLOGY"
    DCRUM_DECODER_TYPE = "DCRUM_DECODER_TYPE"
    ENTITY_ID = "ENTITY_ID"
    HYPERVISOR_TYPE = "HYPERVISOR_TYPE"
    INDEXED_NAME = "INDEXED_NAME"
    INDEXED_STRING = "INDEXED_STRING"
    INDEXED_TAG = "INDEXED_TAG"
    INTEGER = "INTEGER"
    IP_ADDRESS = "IP_ADDRESS"
    MOBILE_PLATFORM = "MOBILE_PLATFORM"
    OS_ARCHITECTURE = "OS_ARCHITECTURE"
    OS_TYPE = "OS_TYPE"
    PAAS_TYPE = "PAAS_TYPE"
    SERVICE_TOPOLOGY = "SERVICE_TOPOLOGY"
    SERVICE_TYPE = "SERVICE_TYPE"
    SIMPLE_HOST_TECH = "SIMPLE_HOST_TECH"
    SIMPLE_TECH = "SIMPLE_TECH"
    STRING = "STRING"
    SYNTHETIC_ENGINE_TYPE = "SYNTHETIC_ENGINE_TYPE"
    TAG = "TAG"
    NONE = None


class ManagementZoneRuleType(Enum):
    APPLICATION = "APPLICATION"
    AWS_APPLICATION_LOAD_BALANCER = "AWS_APPLICATION_LOAD_BALANCER"
    AWS_CLASSIC_LOAD_BALANCER = "AWS_CLASSIC_LOAD_BALANCER"
    AWS_NETWORK_LOAD_BALANCER = "AWS_NETWORK_LOAD_BALANCER"
    AWS_RELATIONAL_DATABASE_SERVICE = "AWS_RELATIONAL_DATABASE_SERVICE"
    AZURE = "AZURE"
    CUSTOM_APPLICATION = "CUSTOM_APPLICATION"
    CUSTOM_DEVICE = "CUSTOM_DEVICE"
    DCRUM_APPLICATION = "DCRUM_APPLICATION"
    ESXI_HOST = "ESXI_HOST"
    EXTERNAL_SYNTHETIC_TEST = "EXTERNAL_SYNTHETIC_TEST"
    HOST = "HOST"
    HTTP_CHECK = "HTTP_CHECK"
    MOBILE_APPLICATION = "MOBILE_APPLICATION"
    PROCESS_GROUP = "PROCESS_GROUP"
    SERVICE = "SERVICE"
    SYNTHETIC_TEST = "SYNTHETIC_TEST"
    WEB_APPLICATION = "WEB_APPLICATION"
    WEB_APPLICATION_NAME = "WEB_APPLICATION_NAME"
    NONE = None


class ComparisonBasic(DynatraceObject):
    def _create_from_raw_data(self, raw_element: Dict[str, Any]):
        self.operator: str = raw_element.get("operator")
        self.value: dict = raw_element.get("value")
        self.negate: bool = raw_element.get("negate")
        self.type: ComparisonBasicType = ComparisonBasicType(raw_element.get("type"))
        self.case_sensitive: bool = raw_element.get("caseSensitive")


class ConditionKey(DynatraceObject):
    def _create_from_raw_data(self, raw_element: Dict[str, Any]):
        self.attribute: ConditionKeyAttribute = ConditionKeyAttribute(raw_element.get("attribute"))
        self.type: ConditionKeyType = ConditionKeyType(raw_element.get("type"))


class EntityRuleEngineCondition(DynatraceObject):
    def _create_from_raw_data(self, raw_element: Dict[str, Any]):
        self.key: ConditionKey = ConditionKey(raw_element=raw_element.get("key"))
        self.comparison_info: ComparisonBasic = ComparisonBasic(raw_element=raw_element.get("comparisonInfo"))


class EntitySelectorBasedManagementZoneRule(DynatraceObject):
    def _create_from_raw_data(self, raw_element: Dict[str, Any]):
        self.enabled: bool = raw_element.get("enabled")
        self.entity_selector: str = raw_element.get("entitySelector")
        self.value_format: str = raw_element.get("valueFormat")


class ManagementZoneRule(DynatraceObject):
    def _create_from_raw_data(self, raw_element: Dict[str, Any]):
        self.type: ManagementZoneRuleType = ManagementZoneRuleType(raw_element.get("type"))
        self.enabled: bool = raw_element.get("enabled")
        self.value_format: str = raw_element.get("valueFormat")
        self.propagation_types: List[PropagationType] = [PropagationType(prop_type) for prop_type in (raw_element.get("propagationTypes") or [])]
        self.conditions: List[EntityRuleEngineCondition] = [
            EntityRuleEngineCondition(raw_element=condition) for condition in (raw_element.get("conditions") or [])
        ]


class ManagementZone(DynatraceObject):
    def _create_from_raw_data(self, raw_element: Dict[str, Any]):
        self.metadata: ConfigurationMetadata = ConfigurationMetadata(self._http_client, None, raw_element.get("metadata"))
        self.id: str = raw_element.get("id")
        self.name: str = raw_element.get("name")
        self.description: str = raw_element.get("description")
        self.rules: List[ManagementZoneRule] = [ManagementZoneRule(raw_element=rule) for rule in raw_element.get("rules")]
        self.entity_selector_based_rules: List[EntitySelectorBasedManagementZoneRule] = [
            EntitySelectorBasedManagementZoneRule(raw_element=rule) for rule in (raw_element.get("entitySelectorBasedRules") or [])
        ]


class ManagementZoneShortRepresentation(EntityShortRepresentation):
    def get_full_configuration(self):
        """
        Get the full configuration for this management zone short representation.
        """
        response = self._http_client.make_request(f"{ManagementZoneService.ENDPOINT}_{self.id}").json()
        return ManagementZone(http_client=self._http_client, raw_element=response)
