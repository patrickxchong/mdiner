const mongoose = require('mongoose');

const { Schema } = mongoose;

const PractitionerSchema = new Schema({
  Name: {
    type: String,
    required: true,
  },
  SpecialisedIn: {
    type: String,
  },
  Rating: {
    type: Number,
    min: 0,
    max: 5,
    required: true,
  },
});

const ClinicSchema = new Schema({
  Name: {
    type: String,
    required: true,
  },
  Rating: {
    type: Number,
    min: 0,
    max: 5,
    required: true,
  },
});

const PNCSchema = new Schema({
  ClinicID: { type: Schema.Types.ObjectId, ref: 'Clinic' },
  PractitionerID: { type: Schema.Types.ObjectId, ref: 'Practitioner' },
});

const Practitioner = mongoose.model('Practitioner', PractitionerSchema);
const Clinic = mongoose.model('Clinic', ClinicSchema);
const PNC = mongoose.model('PNC', PNCSchema);

module.exports = Practitioner;
module.exports = Clinic;
module.exports = PNC;
