import * as React from 'react';

const MyCustomWidget = (props: any) => {
  return (
    <input
      type="text"
      className="custom"
      value={props.value}
      required={props.required}
      onChange={event => props.onChange(event.target.value)}
    />
  );
};

const myWidgets = {
  myCustomWidget: MyCustomWidget
};

const ThemeObject = {
  widgets: myWidgets
};

export default ThemeObject;
