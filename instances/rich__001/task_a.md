Improve right-padding behavior for styled `Text` segments.

When a `Text` object has an inline style span that ends at the current end of
the string, `pad_right()` should extend that span over the added padding
characters. This keeps styled cells visually continuous when padding is used to
align content.
