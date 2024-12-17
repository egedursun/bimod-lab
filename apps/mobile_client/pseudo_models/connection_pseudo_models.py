#  Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
#  Project: Bimod.io™
#  File: connection_pseudo_models.py
#  Last Modified: 2024-11-26 16:03:05
#  Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
#  Created: 2024-11-26 16:03:06
#
#  This software is proprietary and confidential. Unauthorized copying,
#  distribution, modification, or use of this software, whether for
#  commercial, academic, or any other purpose, is strictly prohibited
#  without the prior express written permission of BMD™ Autonomous
#  Holdings.
#
#   For permission inquiries, please contact: admin@Bimod.io.
#

import uuid

from django.utils import timezone


class MobileClientConnection__PseudoModel:
    class MobileClientConnection__Chat__PseudoModel:

        class MobileClientConnection__Chat__Message__PseudoModel:

            def __init__(
                self,
                message_role: str,
                message_text: str,
                message_files: list = None,
                message_images: list = None
            ):
                self.message_role: str = message_role
                self.message_text: str = message_text
                self.message_files: list = message_files
                self.message_images: list = message_images

                self.sent_at: str = timezone.now().strftime("%Y-%m-%d %H:%M:%S")

            @staticmethod
            def map_to_dict(instance):
                object_dict = {}

                for attr in instance.__dict__:
                    object_dict[attr] = getattr(
                        instance,
                        attr
                    )

                return object_dict

            @staticmethod
            def map_to_dicts(object_instances):
                return [
                    MobileClientConnection__PseudoModel.
                    MobileClientConnection__Chat__PseudoModel.

                    MobileClientConnection__Chat__Message__PseudoModel.map_to_dict(
                        object_instance
                    ) for object_instance in object_instances
                ]

            @staticmethod
            def map_to_object(object_dict):
                return (
                    MobileClientConnection__PseudoModel.
                    MobileClientConnection__Chat__PseudoModel.
                    MobileClientConnection__Chat__Message__PseudoModel(
                        message_role=object_dict.get('message_role'),
                        message_text=object_dict.get('message_text'),
                        message_files=object_dict.get('message_files'),
                        message_images=object_dict.get('message_images')
                    )
                )

            @staticmethod
            def map_to_objects(object_dicts):
                return [
                    MobileClientConnection__PseudoModel.
                    MobileClientConnection__Chat__PseudoModel.
                    MobileClientConnection__Chat__Message__PseudoModel.
                    map_to_object(
                        object_dict
                    ) for object_dict in object_dicts
                ]

            def build__universal_instance(self):
                dict_instance = (
                    MobileClientConnection__PseudoModel.
                    MobileClientConnection__Chat__PseudoModel.
                    MobileClientConnection__Chat__Message__PseudoModel.map_to_dict(
                        self
                    )
                )
                return dict_instance

        #############################################################################################################
        #############################################################################################################

        def __init__(self):
            self.uuid = str(uuid.uuid4())
            self.created_at: str = timezone.now().strftime("%Y-%m-%d %H:%M:%S")
            self.messages: list[
                MobileClientConnection__PseudoModel
                .MobileClientConnection__Chat__PseudoModel
                .MobileClientConnection__Chat__Message__PseudoModel
            ] = []

        @staticmethod
        def map_to_dict(instance):
            object_dict = {}

            for attr in instance.__dict__:
                object_dict[attr] = getattr(
                    instance,
                    attr
                )

            return object_dict

        @staticmethod
        def map_to_dicts(object_instances):
            return [
                MobileClientConnection__PseudoModel.
                MobileClientConnection__Chat__PseudoModel.map_to_dict(
                    object_instance
                ) for object_instance in object_instances
            ]

        @staticmethod
        def map_to_object(object_dict):
            return (
                MobileClientConnection__PseudoModel.
                MobileClientConnection__Chat__PseudoModel()
            )

        @staticmethod
        def map_to_objects(object_dicts):
            return [
                MobileClientConnection__PseudoModel
                .MobileClientConnection__Chat__PseudoModel
                .map_to_object(
                    object_dict
                ) for object_dict in object_dicts
            ]

        def build__universal_instance(self):
            dict_instance = (
                MobileClientConnection__PseudoModel
                .MobileClientConnection__Chat__PseudoModel.map_to_dict(
                    self)
            )
            return dict_instance

    #############################################################################################################
    #############################################################################################################

    def __init__(
        self,
        connection_type: str,
        connection_endpoint: str,
        connection_is_public: bool,
        connection_api_key: str = None
    ):
        self.connection_type: str = connection_type
        self.connection_endpoint: str = connection_endpoint
        self.connection_is_public: bool = connection_is_public
        self.connection_api_key: str = connection_api_key

        self.created_at: str = timezone.now().strftime("%Y-%m-%d %H:%M:%S")

        self.chats: list[
            MobileClientConnection__PseudoModel
            .MobileClientConnection__Chat__PseudoModel
        ] = []

    @staticmethod
    def map_to_dict(instance):
        object_dict = {}

        for attr in instance.__dict__:
            object_dict[attr] = getattr(
                instance,
                attr
            )

        return object_dict

    @staticmethod
    def map_to_dicts(object_instances):
        return [
            MobileClientConnection__PseudoModel.map_to_dict(
                object_instance
            ) for object_instance in object_instances
        ]

    @staticmethod
    def map_to_object(object_dict):
        return MobileClientConnection__PseudoModel(
            connection_type=object_dict.get(
                'connection_type'
            ),

            connection_endpoint=object_dict.get(
                'connection_endpoint'
            ),

            connection_is_public=object_dict.get(
                'connection_is_public'
            ),

            connection_api_key=object_dict.get(
                'connection_api_key'
            )
        )

    @staticmethod
    def map_to_objects(object_dicts):
        return [
            MobileClientConnection__PseudoModel.map_to_object(
                object_dict
            ) for object_dict in object_dicts
        ]

    def build__universal_instance(self):
        dict_instance = MobileClientConnection__PseudoModel.map_to_dict(
            self
        )

        return dict_instance
