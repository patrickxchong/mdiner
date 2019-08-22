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
  CumulativeRating: {
    type: Number,
    min: 0,
    max: 5,
  },
});

const ClinicSchema = new Schema({
  Name: {
    type: String,
    required: true,
  },
  CumulativeRating: {
    type: Number,
    min: 0,
    max: 5,
  },
});

const PNCSchema = new Schema({
  ClinicID: { type: Schema.Types.ObjectId, ref: 'Clinic' },
  PractitionerID: { type: Schema.Types.ObjectId, ref: 'Practitioner' },
});

const Practitioner = mongoose.model('Practitioner', PractitionerSchema);
const Clinic = mongoose.model('Clinic', ClinicSchema);
const PNC = mongoose.model('PNC', PNCSchema);

exports.Practitioner = Practitioner;
exports.Clinic = Clinic;
exports.PNC = PNC;
