// Emergency Post Recovery Script
// Open browser console (F12) and paste this code to check for lost posts

console.log('=== CHECKING FOR LOST POSTS ===');

const savedDatabase = localStorage.getItem('blogDatabase');
if (savedDatabase) {
    const localDB = JSON.parse(savedDatabase);
    console.log('Posts found in localStorage:', localDB.posts.length);
    
    localDB.posts.forEach((post, index) => {
        console.log(`\nPost ${index + 1}:`);
        console.log(`ID: ${post.id}`);
        console.log(`Title: ${post.title}`);
        console.log(`Status: ${post.status}`);
        console.log(`Date: ${post.date}`);
        console.log(`Content preview: ${post.content.substring(0, 100)}...`);
    });
    
    // Create downloadable file
    const dataStr = JSON.stringify(localDB, null, 2);
    const dataBlob = new Blob([dataStr], {type: 'application/json'});
    const link = document.createElement('a');
    link.href = URL.createObjectURL(dataBlob);
    link.download = 'recovered-blog-database.json';
    link.click();
    
    console.log('\n=== DOWNLOAD STARTED ===');
    console.log('A file "recovered-blog-database.json" should have been downloaded.');
    console.log('Replace your server\'s blog-database.json with this file.');
} else {
    console.log('No posts found in localStorage');
}
