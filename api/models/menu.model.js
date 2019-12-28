const mongoose = require("mongoose");

const MenuSchema = mongoose.Schema(
  {
    id: String,
    meals: String
  },
  {
    timestamps: true
  }
);

module.exports = mongoose.model("Menu", MenuSchema);
