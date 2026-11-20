from check_sitemap_urls import served_directly


def test_trailing_slash_url_needs_index_html(tmp_path):
    (tmp_path / "a" / "b").mkdir(parents=True)
    (tmp_path / "a" / "b" / "index.html").write_text("x")
    assert served_directly(tmp_path, "https://doc.yupitek.com/a/b/")


def test_url_without_slash_redirects_when_built_as_directory(tmp_path):
    (tmp_path / "a" / "b").mkdir(parents=True)
    (tmp_path / "a" / "b" / "index.html").write_text("x")
    assert not served_directly(tmp_path, "https://doc.yupitek.com/a/b")


def test_url_without_slash_is_served_from_html_file(tmp_path):
    (tmp_path / "a").mkdir()
    (tmp_path / "a" / "b.html").write_text("x")
    assert served_directly(tmp_path, "https://doc.yupitek.com/a/b")


def test_root(tmp_path):
    (tmp_path / "index.html").write_text("x")
    assert served_directly(tmp_path, "https://doc.yupitek.com/")
