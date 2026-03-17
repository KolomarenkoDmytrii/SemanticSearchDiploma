import React from 'react';
import Dropdown from 'react-bootstrap/Dropdown';
import { useTranslation } from 'react-i18next';

import { lngNames } from './config';

// const LanguageItem = React.forwardRef(({ children, onClick }, ref) => {
//     const { t, i18n } = useTranslation();

//     return <a
//         href=""
//         ref={ref}
//         onClick={(e) => {
//             e.preventDefault();
//             i18n.changeLanguage(lngCode);
//         }}
//     >
//         {lngName}
//     </a>;
// });

function LanguageSwitcher() {
    const { t, i18n } = useTranslation();

    return (
        <Dropdown>
            <Dropdown.Toggle id='language-switcher' className='btn btn-primary dropdown-toggle' type='button'>
                {t('language')}
            </Dropdown.Toggle>

            <Dropdown.Menu>
                {Object.keys(lngNames).map((lngCode) =>
                (<Dropdown.Item
                    key={lngCode}
                    onClick={() => i18n.changeLanguage(lngCode)}
                >
                    {lngNames[lngCode]}
                </Dropdown.Item>))}
            </Dropdown.Menu>
        </Dropdown>
    );
}

export default LanguageSwitcher;
