from utils.http_client import create_session, get_page


def test_books_website():
    session = create_session()

    response = get_page(
        session,
        "https://books.toscrape.com/"
    )

    assert response.status_code == 200