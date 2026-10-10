const fs = require('fs');

async function fetchAllAttachments() {
  const token = 'YOUR_ACCESS_TOKEN_HERE';
  let page = 1;
  let allData = [];
  let hasMore = true;

  try {
    while (hasMore) {
      // Using limit=100 or your desired page size
      const url = `https://your-api-domain.com/api/attachments?level=1&page=${page}&limit=100`;
      
      const response = await fetch(url, {
        method: 'GET',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        }
      });

      if (!response.ok) {
        throw new Error(`HTTP error! Status: ${response.status}`);
      }

      const json = await response.json();
      const items = json.data || [];
      
      allData.push(...items);

      // Check if we've fetched all items based on the total property
      if (allData.length >= json.total || items.length === 0) {
        hasMore = false;
      } else {
        page++;
      }
    }

    fs.writeFileSync('all-attachments.json', JSON.stringify({ data: allData, total: allData.length }, null, 2));
    console.log(`Successfully saved all ${allData.length} records to all-attachments.json`);
  } catch (error) {
    console.error('Error fetching data:', error);
  }
}

fetchAllAttachments();