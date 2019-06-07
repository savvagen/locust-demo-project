// index.js

module.exports = () => {

  const data = { posts: [], users: [], comments: [] }


  // Create 1000 users
  for (let i = 0; i < 1000; i++) {
    data.users.push({ id: i, name: `user${i}` })
  }


  // Create 100 posts
  for (let i = 0; i < 100; i++) {
    data.posts.push({ id: i, title: `post ${i}`, body: `Hello This is a post ${i}`,  author: i })
  }


  //Create 100 comments
  for (let i = 0; i < 100; i++){
    data.comments.push({ id: i, author: data.users[i].name, body: `This is a comment ${i}`, postId: i })
  }

  return data
}
