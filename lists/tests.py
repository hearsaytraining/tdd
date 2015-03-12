from django.template.loader import render_to_string
# Create your tests here.
	
	def test_home_page_returns_correct_html(self):	
		request = HttpRequest()
			response = home_page(request)
			expect_html = render_to_string('home.html')
			self.assertEqual(response.content.decode(), expected_html)
