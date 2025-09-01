chrome.runtime.onInstalled.addListener(() => {
  console.log('Chrome extension installed');
});

chrome.action.onClicked.addListener((tab) => {
  console.log('Extension icon clicked', tab);
});