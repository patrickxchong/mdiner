const PractitionerModel = require('../models/practitioner.model.js');

const { Practitioner, Clinic, PNC } = PractitionerModel;

// Create and Save a new Note
exports.create = (req, res) => {
  console.log(req.body); // eslint-disable-line no-console
  // Validate request
  // if (!req.body.content) {
  //   return res.status(400).send({
  //     message: 'Req can not be empty',
  //   });
  // }

  // Create a Note
  const practitioner = new Practitioner({
    Name: req.body.practitionerName,
    SpecialisedIn: req.body.specialisedIn,
  });

  const clinic = new Clinic({
    Name: req.body.clinicName,
  });
  /* eslint no-underscore-dangle: ["error", { "allow": ["_id"] } ] */
  const pnc = new PNC({
    ClinicID: clinic._id,
    PractitionerID: practitioner._id,
  });

  // Save Note in the database
  practitioner.save().then((practitionerData) => {
    clinic.save().then((clinicData) => {
      pnc.save().then((pncData) => {
        res.send([practitionerData, clinicData, pncData]);
      });
    });
  })
    .catch((err) => {
      res.status(500).send({
        message: err.message || 'Some error occurred while creating the Note.',
      });
    });
  return 0;
};

// Retrieve and return all notes from the database.
exports.findAll = (req, res) => {
  Practitioner.find().then((practitionerData) => {
    Clinic.find().then((clinicData) => {
      PNC.find().then((pncData) => {
        res.send([practitionerData, clinicData, pncData]);
      });
    });
  })
    .catch((err) => {
      res.status(500).send({
        message: err.message || 'Some error occurred while finding Notes.',
      });
    });
};


// Delete a note with the specified noteId in the request
exports.delete = (req, res) => {
  Practitioner.findByIdAndRemove(req.params.practitionerID)
    .then((note) => {
      if (!note) {
        return res.status(404).send({
          message: `Note not found with id ${req.params.practitionerID}`,
        });
      }
      res.send({ message: 'Note deleted successfully!' });
      return 0;
    })
    .catch((err) => {
      if (err.kind === 'ObjectId' || err.name === 'NotFound') {
        return res.status(404).send({
          message: `Note not found with id ${req.params.practitionerID}`,
        });
      }
      return res.status(500).send({
        message: `Could not delete note with id ${req.params.practitionerID}`,
      });
    });
};
