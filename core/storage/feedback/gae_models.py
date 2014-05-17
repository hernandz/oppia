# coding: utf-8
#
# Copyright 2014 The Oppia Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS-IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Models for Oppia feedback threads and messages."""

__author__ = 'Koji Ashida'

from core.platform import models
(base_models,) = models.Registry.import_models([models.NAMES.base_model])
import utils

from google.appengine.ext import ndb

STATUS_CHOICES_OPEN = 'open'
STATUS_CHOICES_FIXED = 'fixed'
STATUS_CHOICES_IGNORED = 'ignored'
STATUS_CHOICES_DUPLICATE = 'duplicate'
STATUS_CHOICES_COMPLIMENT = 'compliment'
STATUS_CHOICES_NOT_ACTIONABLE = 'not_actionable'
STATUS_CHOICES = [
    STATUS_CHOICES_OPEN,
    STATUS_CHOICES_FIXED,
    STATUS_CHOICES_IGNORED,
    STATUS_CHOICES_DUPLICATE,
    STATUS_CHOICES_COMPLIMENT,
    STATUS_CHOICES_NOT_ACTIONABLE,
]


class FeedbackThreadModel(base_models.BaseModel):
    """Threads for each exploration.

    The id/key of instances of this class has the form
        [EXPLORATION_ID].[THREAD_ID]
    """
    # ID of the exploration the thread is about.
    exploration_id = ndb.StringProperty(required=True, indexed=True)
    # ID of state the thread is for. Does not exist if the thread is about the
    # entire exploration.
    state_id = ndb.StringProperty(indexed=True)
    # ID of the user who started the thread.
    original_author_id = ndb.StringProperty(required=True, indexed=True)
    # Latest status of the thread.
    status = ndb.StringProperty(
        default=STATUS_CHOICES_OPEN,
        choices=STATUS_CHOICES,
        required=True,
        indexed=True,
    )
    # Latest subject of the thread.
    subject = ndb.StringProperty(indexed=False)
    # Summary text of the thread.
    summary = ndb.TextProperty(indexed=False)

    @classmethod
    def generate_new_thread_id(cls, exploration_id):
        """Generates a new thread id, unique within the exploration.

        Exploration ID + the generated thread ID is globally unique.
        """
        MAX_RETRIES = 10
        RAND_RANGE = 127 * 127
        for i in range(MAX_RETRIES):
            thread_id = utils.base64_from_int(utils.get_epoch_time()) + 
                utils.base64_from_int(utils.get_random_int(RAND_RANGE))
            if not cls.get(exploration_id, thread_id):
                return new_id
        raise Exception(
            'New thread id generator is producing too many collisions.')

    @classmethod
    def _generate_id(cls, exploration_id, thread_id):
        return '.'.join([exploration_id, thread_id])

    @classmethod
    def create(cls, exploration_id, thread_id):
        """Creates a new FeedbackThreadModel entry.

        Throws an exception if a thread with the given exploration ID and
        thread ID combination exists already.
        """
        instance_id = cls._generate_id(exploration_id, thread_id)
        if cls.get_by_id(instance_id):
          raise Exception(
              'Feedback thread ID conflict on create.')
        return cls(id=instance_id)

    @classmethod
    def get(cls, exploration_id, thread_id):
        """Gets the FeedbackThreadModel entry for the given ID.

        Returns None if the thread is not found or is already deleted.
        """
        instance_id = cls._generate_id(exploration_id, thread_id)
        return super(FeedbackThreadModel, cls).get(instance_id)


class FeedbackMessageModel(base_models.BaseModel):
    """Feedback messages. One or more of these messages make a thread.

    The id/key of instances of this class has the form
        [EXPLORATION_ID].[THREAD_ID].[MESSAGE_ID]
    """
    # ID corresponding to an entry of FeedbackThreadModel in the form of 
    #   [EXPLORATION_ID].[THREAD_ID]
    thread_id = ndb.StringProperty(required=True, indexed=True)
    # 0-based sequential numerical ID. Sorting by this field will create the
    # thread in chronological order.
    message_id = ndb.IntegerProperty(required=True, indexed=True)
    # ID of the user who posted this message.
    author_id = ndb.StringProperty(required=True, indexed=True)
    # New thread status. Must exist in the first message of a thread. For the
    # rest of the thread, should exist only when the status changes.
    updated_status = ndb.StringProperty(choices=STATUS_CHOICES, indexed=True)
    # New thread subject. Must exist in the first message of a thread. For the
    # rest of the thread, should exist only when the subject changes.
    updated_subject = ndb.StringProperty(indexed=False)
    # Message text. Allowed not to exist (e.g. post only to update the status).
    text = ndb.StringProperty(indexed=False)

    @classmethod
    def _generate_id(cls, thread_id, message_id):
        return '.'.join([thread_id, message_id])

    @classmethod
    def create(cls, thread_id, message_id):
        """Creates a new FeedbackMessageModel entry.

        Throws an exception if a message with the given thread ID and message ID
        combination exists already.
        """
        instance_id = cls._generate_id(thread_id, message_id)
        if cls.get_by_id(instance_id):
          raise Exception(
              'Feedback message ID conflict on create.')
        return cls(id=instance_id)

    @classmethod
    def get(cls, thread_id, message_id):
        """Gets the FeedbackMessageModel entry for the given ID.

        Returns None if the message is not found or is already deleted.
        """
        instance_id = cls._generate_id(thread_id, message_id)
        return super(FeedbackMessageModel, cls).get(instance_id)