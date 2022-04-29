const Storage = Capacitor.Plugins.Storage;
const Modals = Capacitor.Plugins.Modals;
const App = Capacitor.Plugins.App;

async function getItem(key) {
  let { value } = await Storage.get({ key })
  return value;
}

async function setItem(key, value) {
  return await Storage.set({ key, value });
}

async function showAlert(title, message) {
  let alertRet = await Modals.alert({
    title,
    message
  });
}

async function showConfirm(title, message) {
  let confirmRet = await Modals.confirm({
    title,
    message
  });
  console.log('Confirm ret', confirmRet);
  return confirmRet.value;
}

async function showPrompt() {
  let promptRet = await Modals.prompt({
    title: 'Hello',
    message: 'What\'s your name?'
  });
  console.log('Prompt ret', promptRet);
}

async function showActions() {
  let promptRet = await Modals.showActions({
    title: 'Photo Options',
    message: 'Select an option to perform',
    options: [
      {
        title: 'Upload'
      },
      {
        title: 'Share'
      },
      {
        title: 'Remove',
        // style: ActionSheetOptionStyle.Destructive
      }
    ]
  })
  console.log('You selected', promptRet);
}

App.addListener("backButton", async (data) => {
  if (!window.location.search) { // if no query string, means at homepage
    const result = await showConfirm('Confirm', 'Are you sure you would like to exit?')
    if (result) {
      App.exitApp();
    }
  } else {
    window.history.back();
  }
}) 
