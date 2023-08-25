const sortSelectElement = document.querySelector('#sort-select');

sortSelectElement.addEventListener('change', (event) => {
  const selectedOption = event.target.options[event.target.selectedIndex];
  
  const url = new URL(window.location.href);
  const queryParams = new URLSearchParams(url.search);
  
  queryParams.set('sort', selectedOption.value);
  
  const sidoParam = queryParams.get('sido');
  const gugunParam = queryParams.get('gugun');
  const searchQueryParam = queryParams.get('search_query');
  
  if (sidoParam) queryParams.set('sido', sidoParam);
  if (gugunParam) queryParams.set('gugun', gugunParam);
  if (searchQueryParam) queryParams.set('search_query', searchQueryParam);
  
  url.search = queryParams.toString();
  
  window.location.href = url.href;
});