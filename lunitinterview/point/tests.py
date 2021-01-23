import base64

from django.test import TestCase, Client
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase, APIClient

from point.models import Point


class PointTests(APITestCase):

    expected_data = {
            "points": [
                {
                    "id": 1,
                    "data": {
                        "type": "Point",
                        "coordinates": [
                            0,
                            0
                        ]
                    }
                },
                {
                    "id": 2,
                    "data": {
                        "type": "Point",
                        "coordinates": [
                            10,
                            0
                        ]
                    }
                },
                {
                    "id": 3,
                    "data": {
                        "type": "Point",
                        "coordinates": [
                            20,
                            0
                        ]
                    }
                },
                {
                    "id": 4,
                    "data": {
                        "type": "Point",
                        "coordinates": [
                            30,
                            0
                        ]
                    }
                },
                {
                    "id": 5,
                    "data": {
                        "type": "Point",
                        "coordinates": [
                            40,
                            0
                        ]
                    }
                },
                {
                    "id": 6,
                    "data": {
                        "type": "Point",
                        "coordinates": [
                            50,
                            0
                        ]
                    }
                },
                {
                    "id": 7,
                    "data": {
                        "type": "Point",
                        "coordinates": [
                            60,
                            0
                        ]
                    }
                },
                {
                    "id": 8,
                    "data": {
                        "type": "Point",
                        "coordinates": [
                            70,
                            0
                        ]
                    }
                },
                {
                    "id": 9,
                    "data": {
                        "type": "Point",
                        "coordinates": [
                            80,
                            0
                        ]
                    }
                },
                {
                    "id": 10,
                    "data": {
                        "type": "Point",
                        "coordinates": [
                            90,
                            0
                        ]
                    }
                }
            ]
        }
    def setUp(self) -> None:
        url = reverse('point-list')
        for i in range(0,10):
            longitude = 10*i
            data = {
                "data": {
                    "type": "Point",
                    "coordinates": [longitude, 0]
                }

            }
            self.client.post(url, data, format='json')

    def test_create_point(self):
        """
        Ensure we can create a point object.
        """
        url = reverse('point-list')
        data = {
            "data": {
                "type": "Point",
                "coordinates": [50, 0]
            }
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_retrieve_points(self):
        """
        Ensure we can retrive a point
        """
        url = reverse('point-list')

        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, self.expected_data)

    def test_retrieve_paginated_points(self):
        """
        Ensure we can retrieve a paginated points
        """
        url = reverse('point-list')
        data = {
            "data": {
                "type": "Point",
                "coordinates": [-10, 0]
            }

        }
        self.client.post(url, data, format='json')

        response = self.client.get(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, self.expected_data)

    def test_retrieve_single_point(self):
        """
        Ensure we can retrieve a single point.
        """
        url = "/points/1/"
        data = {
            "id": 1,
            "data": {
                "type": "Point",
                "coordinates": [
                    0,
                    0
                ]
            }
        }
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, data)

    def test_update_point(self):
        """
        Ensure we can update a point object.
        """
        url = "/points/1/"
        data = {
            "data": {
                "type": "Point",
                "coordinates": [50, 0]
            }
        }
        expected_data = {
            "id": 1,
            "data": {
                "type": "Point",
                "coordinates": [
                    50,
                    0
                ]
            }
        }
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, expected_data)
