const practitioner = require('../controllers/practitioner.controller.js');

module.exports = (app) => {
  // Create a new Note
  app.post('/api/practitioner', practitioner.create);
  // Retrieve all Notes
  app.get('/api/practitioner', practitioner.findAll);
  // Delete a Note with practitionerID
  app.delete('/api/practitioner/:practitionerID', practitioner.delete);
};
