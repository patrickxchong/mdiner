const mongoose = require('mongoose');

const MenuSchema = mongoose.Schema(
  {
    content: String,
  },
  {
    timestamps: true,
  },
);

module.exports = mongoose.model('Menu', MenuSchema);
