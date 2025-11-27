from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from django.contrib.auth.models import User
from datetime import date
from unittest.mock import patch

from api.models import Author, Book
from api.serializers import BookSerializer

# =========================================================================
# Setup Helper Functions
# =========================================================================

class BookAPITestCase(APITestCase):
    """
    Base class for testing the Book API endpoints.
    Initializes test data (Author, Book) and sets up authenticated/unauthenticated clients.
    """
    def setUp(self):
        # 1. Test Users
        self.user = User.objects.create_user(username='tester', password='password123')
        self.staff_user = User.objects.create_user(username='staff', password='staffpassword', is_staff=True)

        # 2. Test Data
        self.author = Author.objects.create(name="F. Scott Fitzgerald")
        self.book1 = Book.objects.create(
            title="The Great Gatsby",
            publication_year=1925,
            author=self.author
        )
        self.book2 = Book.objects.create(
            title="Tender is the Night",
            publication_year=1934,
            author=self.author
        )

        # 3. URL Names (Defined in api/urls.py)
        self.list_create_url = reverse('book-list-create')
        self.detail_url = reverse('book-detail', kwargs={'pk': self.book1.pk})
        self.update_url = reverse('book-update', kwargs={'pk': self.book1.pk})
        self.delete_url = reverse('book-delete', kwargs={'pk': self.book1.pk})

        # 4. Clients
        self.client = APIClient()
        self.auth_client = APIClient()
        # Authenticate the client for writing/deleting tests
        self.auth_client.force_authenticate(user=self.user)

# =========================================================================
# Test Cases for Read Operations (Accessible to All Users)
# =========================================================================

class BookReadTests(BookAPITestCase):
    """Tests GET requests (List and Detail)"""

    def test_list_books_unauthenticated(self):
        """Ensure unauthenticated user can retrieve the list of books (Read-Only permission)."""
        response = self.client.get(self.list_create_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        # Verify the structure using the serializer
        expected_data = BookSerializer([self.book1, self.book2], many=True).data
        self.assertEqual(response.data, expected_data)

    def test_retrieve_book_detail_authenticated(self):
        """Ensure authenticated user can retrieve a specific book."""
        response = self.auth_client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], self.book1.title)

    def test_retrieve_book_not_found(self):
        """Ensure requesting a non-existent book returns 404 Not Found."""
        wrong_url = reverse('book-detail', kwargs={'pk': 999})
        response = self.client.get(wrong_url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


# =========================================================================
# Test Cases for Write Operations (Requires Authentication)
# =========================================================================

class BookCreateTests(BookAPITestCase):
    """Tests POST requests and custom validation"""

    def test_create_book_authenticated_success(self):
        """Ensure authenticated user can successfully create a new book."""
        new_book_data = {
            'title': 'The Last Tycoon',
            'publication_year': 1941,
            'author': self.author.pk  # Use the primary key of the test author
        }
        response = self.auth_client.post(self.list_create_url, new_book_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), 3)
        self.assertEqual(response.data['title'], 'The Last Tycoon')

    def test_create_book_unauthenticated_forbidden(self):
        """Ensure unauthenticated user cannot create a book (403 Forbidden)."""
        new_book_data = {
            'title': 'Unauthorized Book',
            'publication_year': 2000,
            'author': self.author.pk
        }
        response = self.client.post(self.list_create_url, new_book_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Book.objects.count(), 2) # Count remains unchanged

    @patch('api.serializers.date')
    def test_create_book_future_year_validation_failure(self, mock_date):
        """Test custom validation: ensure future publication year is rejected."""
        # Mock the current date to a fixed point in time (e.g., 2024)
        mock_date.today.return_value = date(2024, 1, 1)

        future_data = {
            'title': 'Book from 2025',
            'publication_year': 2025,
            'author': self.author.pk
        }
        response = self.auth_client.post(self.list_create_url, future_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('publication_year', response.data)
        self.assertIn('cannot be in the future', response.data['publication_year'][0])
        self.assertEqual(Book.objects.count(), 2) # Count remains unchanged


# =========================================================================
# Test Cases for Update and Delete Operations (Requires Authentication)
# =========================================================================

class BookUpdateDeleteTests(BookAPITestCase):
    """Tests PUT/PATCH/DELETE requests"""

    def test_update_book_authenticated_success(self):
        """Ensure authenticated user can update a book."""
        updated_data = {
            'title': 'The Great Gatsby (Revised Edition)',
            'publication_year': self.book1.publication_year,
            'author': self.author.pk
        }
        response = self.auth_client.put(self.update_url, updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Retrieve the book from the database to confirm the change
        self.book1.refresh_from_db()
        self.assertEqual(self.book1.title, 'The Great Gatsby (Revised Edition)')

    def test_update_book_unauthenticated_forbidden(self):
        """Ensure unauthenticated user cannot update a book."""
        updated_data = {'title': 'Forbidden Update', 'publication_year': 1925, 'author': self.author.pk}
        response = self.client.patch(self.update_url, updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # Ensure the title was not changed in the database
        self.book1.refresh_from_db()
        self.assertNotEqual(self.book1.title, 'Forbidden Update')

    def test_delete_book_authenticated_success(self):
        """Ensure authenticated user can delete a book."""
        initial_count = Book.objects.count()
        response = self.auth_client.delete(self.delete_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Book.objects.count(), initial_count - 1)
        # Ensure the deleted book is no longer retrievable
        self.assertFalse(Book.objects.filter(pk=self.book1.pk).exists())

    def test_delete_book_unauthenticated_forbidden(self):
        """Ensure unauthenticated user cannot delete a book."""
        initial_count = Book.objects.count()
        response = self.client.delete(self.delete_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        # Ensure count remains the same
        self.assertEqual(Book.objects.count(), initial_count)