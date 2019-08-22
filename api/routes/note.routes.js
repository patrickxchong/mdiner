const notes = require('../controllers/note.controller.js');

module.exports = (app) => {
  // Create a new Note
  app.post('/api/notes', notes.create);

  // Retrieve all Notes
  app.get('/api/notes', notes.findAll);

  // Retrieve a single Note with noteId
  app.get('/api/notes/:noteId', notes.findOne);

  // Update a Note with noteId
  app.put('/api/notes/:noteId', notes.update);

  // Delete a Note with noteId
  app.delete('/api/notes/:noteId', notes.delete);
};
