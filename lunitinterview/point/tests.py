from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase, APIClient


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
        for i in range(0, 10):
            longitude = 10 * i
            data = {
                "data": {
                    "type": "Point",
                    "coordinates": [longitude, 0]
                }

            }
            self.client.post(url, data, format='json')

        url = reverse('contour-list')
        data = {
            "data":
                {"type": "Polygon",
                 "coordinates": [[25, 10.0], [-10, 10], [-10, -10], [25, -10]]
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

    def test_delete_single_point(self):
        """
        Ensure we can delete a single point.
        """
        url = "/points/1/"
        response = self.client.delete(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_inside_api(self):
        data = {"points": [{
            "id": 1,
            "data": {
                "type": "Point",
                "coordinates": [0, 0]
            }},
            {
                "id": 2,
                "data": {
                    "type": "Point",
                    "coordinates": [10, 0]
                }},
            {
                "id": 3,
                "data": {
                    "type": "Point",
                    "coordinates": [20, 0]
                }}
        ]}
        url = "/points?contour=1"
        redirect_url = '/points/?contour=1'
        response = self.client.get(url, format='json')
        self.assertRedirects(response, redirect_url, status_code=301, target_status_code=200)
        response = self.client.get(redirect_url, format='json')
        self.assertEqual(response.data, data)

    def test_inside_api_validation_error(self):
        url = "/points?contour=2"
        redirect_url = '/points/?contour=2'
        response = self.client.get(url, format='json')
        self.assertRedirects(response, redirect_url, status_code=301, target_status_code=400)
        response = self.client.get(redirect_url, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class ContourTests(APITestCase):

    def setUp(self) -> None:
        url = reverse('contour-list')
        data1 = {
            "data":
                {
                    "type": "Polygon",
                    "coordinates": [
                        [0, 0.0], [10.0, 0.0], [10.0, 20.0], [0, 20.0]
                    ]
                }

        }

        self.client.post(url, data1, format='json')
        data2 = {
            "data":
                {
                    "type": "Polygon",
                    "coordinates": [
                        [20.0, 0.0], [5.0, 5.0], [20.0, 10.0], [5, 15], [20, 20], [30, 10]
                    ]
                }

        }
        self.client.post(url, data2, format='json')

        data3 = {
            "data":
                {
                    "type": "Polygon",
                    "coordinates": [
                        [30, 0.0], [40.0, 0.0], [40.0, 20.0], [30, 20.0]
                    ]
                }

        }

        self.client.post(url, data3, format='json')

    def test_create_contour(self):
        """
        Ensure we can create a contour object.
        """
        url = reverse('contour-list')
        data = {
            "data":
                {
                    "type": "Polygon",
                    "coordinates": [
                        [0, 0.0], [40.0, 0.0], [20.0, 50.0]
                    ]
                }

        }

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_retrieve_contours(self):
        """
        Ensure we can retrive contours
        """
        url = reverse('contour-list')

        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve_single_contour(self):
        """
        Ensure we can retrieve a single point.
        """
        url = "/contours/1/"
        data = {
            "id": 1,
            "data": {
                "type": "Polygon",
                "coordinates": [
                    [0, 0.0], [10.0, 0.0], [10.0, 20.0], [0, 20.0]
                ]
            }
        }
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, data)

    def test_update_contour(self):
        """
        Ensure we can update a contour object.
        """
        url = "/contours/1/"
        data = {"data": {
            "type": "Polygon",
            "coordinates": [
                [0, 0.0], [10.0, 0.0], [10.0, 20.0], [0, 40.0]
            ]
        }}

        expected_data = {
            "id": 1,
            "data": {
                "type": "Polygon",
                "coordinates": [
                    [0, 0.0], [10.0, 0.0], [10.0, 20.0], [0, 40.0]
                ]
            }
        }
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, expected_data)

    def test_delete_single_point(self):
        """
        Ensure we can delete a single point.
        """
        url = "/contours/1/"
        response = self.client.delete(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_intersection(self):
        expected_data = {
            "intersections": [
                {
                    "id": 1,
                    "data": {
                        "type": "Polygon",
                        "coordinates": [[0.0, 0.0], [10.0, 0.0], [10.0, 20.0], [0.0, 20.0]]
                    }
                },
                {
                    "id": 2,
                    "data": {
                        "type": "Polygon",
                        "coordinates": [[20.0, 0.0], [5.0, 5.0], [20.0, 10.0], [5, 15], [20, 20], [30, 10]]
                    }
                },
                16.66666666666667
            ]
        }
        url = "/contours/1/intersection?contour=2"
        redirect_url = "/contours/1/intersection/?contour=2"
        response = self.client.get(url, format='json')
        self.assertRedirects(response, redirect_url, status_code=301, target_status_code=200)
        response = self.client.get(redirect_url, format='json')
        self.assertEqual(response.data, expected_data)

    def test_intersection_validataion_error(self):
        url = "/contours/1/intersection?contour=3"
        redirect_url = "/contours/1/intersection/?contour=3"
        response = self.client.get(url, format='json')
        self.assertRedirects(response, redirect_url, status_code=301, target_status_code=400)
        response = self.client.get(redirect_url, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
