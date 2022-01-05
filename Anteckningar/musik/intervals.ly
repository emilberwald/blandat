\version "2.22.1"
\header {
  title = "Intervals"
  tagline = ""
}
\layout {
  indent = 0.0
  \context
  {
    \Score
    \override NonMusicalPaperColumn.line-break-permission = ##f
    \override NonMusicalPaperColumn.page-break-permission = ##f
  }
  \omit Staff.TimeSignature
  \set Staff.explicitKeySignatureVisibility = #end-of-line-invisible
  \set Staff.explicitClefVisibility = #center-invisible
  \set Staff.printKeyCancellation = ##f
  \set Staff.forceClef = ##f
  \set Score.automaticBars = ##f
}

genc =
#(define-music-function
  (music)
  (scheme?)
  #{
    \new Staff
    {
      \bar "||"
      \key ces \major
      s
      \key c \major
      s
      \transpose c cis
      {
        \mark "C♭, C, C♯"
        $music
      }
      \bar "|."
    }
  #}
  )
genflats =
#(define-music-function
  (music)
  (scheme?)
  #{
    \new Staff
    {
      \bar "||"
      s
      \key es \major
      s
      \transpose c e
      {
        \mark "E♭, E"
        $music
      }
      \bar "||"
      \key ges \major
      s
      \transpose c g
      {
        \mark "G♭, G"
        $music
      }
      \bar "||"
      \key bes \major
      s
      \transpose c b
      {
        \mark "B♭, B"
        $music
      }
      \bar "|."
    }
  #}
  )
gensharps =
#(define-music-function
  (music)
  (scheme?)
  #{
    \new Staff
    {
      \bar "||"
      s
      \key des \major
      s
      \transpose c d
      {
        \mark "D♭, D"
        $music
      }
      \bar "||"
      \key f \major
      s
      \transpose c fis
      {
        \mark "F, F♯"
        $music
      }
      \bar "||"
      \key as \major
      s
      \transpose c a
      {
        \mark "A♭, A"
        $music
      }
      \bar "|."
    }
  #})


% SECONDS

minor-seconds = {
  \clef G
  \key c \major
  {
    <<
      \tweak color darkturquoise b,4    \tweak color blue  c2
      \tweak color darkturquoise b2     \tweak color blue  c'4
      \tweak color darkturquoise b'4    \tweak color blue  c''2
      \tweak color darkturquoise b''2   \tweak color blue  c'''4
      \tweak color darkturquoise b'''4  \tweak color blue  c''''2
    >>
  }
  {
    <<
      \tweak color mediumvioletred  e,4     \tweak color red  f,2
      \tweak color mediumvioletred  e'4    \tweak color red   f'2
      \tweak color mediumvioletred  e2     \tweak color red   f4
      \tweak color mediumvioletred  e''2   \tweak color red   f''4
      \tweak color mediumvioletred  e'''4  \tweak color red   f'''2
      \tweak color mediumvioletred  e''''2 \tweak color red   f''''4
    >>
  }
}

% sevenths
major-sevenths = {
  \clef G
  \key c \major
  {
    <<
      {
        <<
          \tweak color blue c,4 \tweak color darkturquoise b,
          \tweak color blue c'4 \tweak color darkturquoise b'
          \tweak color blue c'''4 \tweak color darkturquoise b'''
        >>
      }\\{

        <<
          \tweak color blue c2 \tweak color darkturquoise b
          \tweak color blue c''2 \tweak color darkturquoise b''
          \tweak color blue c''''2 \tweak color darkturquoise b''''
        >>
      }
    >>
  }
  {
    <<
      {
        <<
          \tweak color red f,,4 \tweak color mediumvioletred e,
          \tweak color red f4 \tweak color mediumvioletred e'
          \tweak color red f''4 \tweak color mediumvioletred e'''
        >>
      }\\{

        <<
          \tweak color red f,2 \tweak color mediumvioletred e
          \tweak color red f'2 \tweak color mediumvioletred e''
          \tweak color red f'''2 \tweak color mediumvioletred e''''
        >>
      }
    >>
  }
}

% INVERTED INTERVALS

major-seconds = {
  \clef G
  \key c \major
  {
    <<
      \tweak color blue  c2         \tweak color purple d4
      \tweak color blue  c'4        \tweak color purple d'2
      \tweak color blue  c''2       \tweak color purple d''4
      \tweak color blue  c'''4      \tweak color purple d'''2
      \tweak color blue  c''''2     \tweak color purple d''''4
    >>
  }
  {
    <<
      \tweak color purple d4      \tweak color mediumvioletred  e2
      \tweak color purple d'2     \tweak color mediumvioletred  e'4
      \tweak color purple d''4    \tweak color mediumvioletred  e''2
      \tweak color purple d'''2   \tweak color mediumvioletred  e'''4
      \tweak color purple d''''4  \tweak color mediumvioletred  e''''2
    >>
  }
  {
    <<
      \tweak color red   f,2      \tweak color orange g,4
      \tweak color red   f'2      \tweak color orange g2
      \tweak color red   f4       \tweak color orange g'4
      \tweak color red   f''4     \tweak color orange g''2
      \tweak color red   f'''2    \tweak color orange g'''4
      \tweak color red   f''''4   \tweak color orange g''''2
    >>
  }
  {
    <<
      \tweak color orange g,4     \tweak color yellowgreen a,2
      \tweak color orange g2      \tweak color yellowgreen a4
      \tweak color orange g'4     \tweak color yellowgreen a'2
      \tweak color orange g''2    \tweak color yellowgreen a''4
      \tweak color orange g'''4   \tweak color yellowgreen a'''2
      \tweak color orange g''''2  \tweak color yellowgreen a''''4
    >>
  }
  {
    <<
      \tweak color yellowgreen a,2    \tweak color darkturquoise b,4
      \tweak color yellowgreen a4     \tweak color darkturquoise b2
      \tweak color yellowgreen a'2    \tweak color darkturquoise b'4
      \tweak color yellowgreen a''4   \tweak color darkturquoise b''2
      \tweak color yellowgreen a'''2  \tweak color darkturquoise b'''4
      \tweak color yellowgreen a''''4 \tweak color darkturquoise b''''2
    >>
  }
}

minor-sevenths = {
  \clef G
  \key c \major
  {
    <<
      {
        <<
          \tweak color blue  c,4        \tweak color purple d,,4
          \tweak color blue  c'4        \tweak color purple d4
          \tweak color blue  c'''4      \tweak color purple d''4
        >>
      }\\{

        <<
          \tweak color purple d4      \tweak color mediumvioletred  e,4
          \tweak color purple d''4    \tweak color mediumvioletred  e'4
          \tweak color purple d''''4    \tweak color mediumvioletred  e'''4
        >>
      }
    >>
  }
  {
    <<
      {
        <<
          \tweak color blue  c2         \tweak color purple d,2
          \tweak color blue  c''2       \tweak color purple d'2
          \tweak color blue  c''''2     \tweak color purple d'''2
        >>
      }\\{

        <<
          \tweak color purple d'2     \tweak color mediumvioletred  e2
          \tweak color purple d'''2   \tweak color mediumvioletred  e''2
        >>
      }

    >>
  }
  {
    <<
      {
        <<
          \tweak color red   f,,4     \tweak color orange g,,,4
          \tweak color red   f4     \tweak color orange g,4
          \tweak color red   f''4     \tweak color orange g'4
          \tweak color red   f''''4     \tweak color orange g'''4
        >>
      }\\{

        <<
          \tweak color red   f,2     \tweak color orange g,,2
          \tweak color red   f'2     \tweak color orange g2
          \tweak color red   f'''2   \tweak color orange g''2
        >>
      }
    >>
  }
  {
    <<
      {
        <<
          \tweak color orange g,4     \tweak color yellowgreen a,,4
          \tweak color orange g'4     \tweak color yellowgreen a4
          \tweak color orange g'''4   \tweak color yellowgreen a''4
        >>
      }\\{

        <<
          \tweak color yellowgreen a4     \tweak color darkturquoise b,4
          \tweak color yellowgreen a''4   \tweak color darkturquoise b'4
          \tweak color yellowgreen a''''4 \tweak color darkturquoise b'''4
        >>
      }

    >>
  }
  {
    <<
      {
        <<
          \tweak color orange g,,2    \tweak color yellowgreen a,,,2
          \tweak color orange g2      \tweak color yellowgreen a,2
          \tweak color orange g''2    \tweak color yellowgreen a'2
          \tweak color orange g''''2  \tweak color yellowgreen a'''2
        >>
      }\\{

        <<
          \tweak color yellowgreen a,2     \tweak color darkturquoise b,,2
          \tweak color yellowgreen a'2     \tweak color darkturquoise b2
          \tweak color yellowgreen a'''2   \tweak color darkturquoise b''2
        >>
      }
    >>
  }
}

\score
{
  \header
  {
    piece = "2, M2, major second, stor sekund"
  }
  #(genc major-seconds)
}
\noPageBreak
\score
{
  #(genflats major-seconds)
}
\noPageBreak
\score
{
  #(gensharps major-seconds)
}
\noPageBreak
\score
{
  \header
  {
    piece = "♭7, m7, minor seventh, liten septima"
  }
  #(genc minor-sevenths)
}
\noPageBreak
\score
{
  #(genflats minor-sevenths)
}
\noPageBreak
\score
{
  #(gensharps minor-sevenths)
}
\pageBreak

\score
{
  \header
  {
    piece = "♭2, m2, minor second, liten sekund"
  }
  #(genc minor-seconds)
}
\score
{
  #(genflats minor-seconds)
}
\score
{
  #(gensharps minor-seconds)
}

\score
{
  \header
  {
    piece = "7, M7, major seventh, stor septima"
  }
  #(genc major-sevenths)
}
\score
{
  #(genflats major-sevenths)
}
\score
{
  #(gensharps major-sevenths)
}

\pageBreak

% THIRDS
minor-thirds = {
  \clef G
  \key c \major
  {
    <<
      {
        <<
          \tweak color yellowgreen a,2    \tweak color blue   c
          \tweak color yellowgreen a'2    \tweak color blue   c''
          \tweak color yellowgreen a'''2  \tweak color blue   c''''
        >>
      }\\{

        <<
          \tweak color yellowgreen a4     \tweak color blue   c'
          \tweak color yellowgreen a''4   \tweak color blue   c'''
        >>
      }
    >>
  }
  {
    <<
      {
        <<

          \tweak color darkturquoise b''2 \tweak color purple d'''  \tweak color red f'''
          \tweak color darkturquoise b2   \tweak color purple d'    \tweak color red f'
        >>
      }\\{
        <<
          \tweak color darkturquoise b'4  \tweak color purple d''   \tweak color red f''
          \tweak color darkturquoise b,4  \tweak color purple d     \tweak color red f
        >>
      }
    >>
  }
  {
    <<
      {
        <<
          \tweak color mediumvioletred e2     \tweak color orange g2
          \tweak color mediumvioletred e''2   \tweak color orange g''2
          \tweak color mediumvioletred e''''2 \tweak color orange g''''2
        >>
      }\\{
        <<
          \tweak color mediumvioletred e,4    \tweak color orange g,4
          \tweak color mediumvioletred e'4    \tweak color orange g'4
          \tweak color mediumvioletred e'''4  \tweak color orange g'''4
        >>
      }
    >>
  }
}

major-sixths = {
  \clef G
  \key c \major
  {
    <<
      \tweak color yellowgreen a4     \tweak color blue   c2
      \tweak color yellowgreen a''4   \tweak color blue   c''2
      \tweak color yellowgreen a''''4   \tweak color blue   c''''2
    >>
  }
  {
    <<
      \tweak color yellowgreen a,2    \tweak color blue   c,4
      \tweak color yellowgreen a'2    \tweak color blue   c'4
      \tweak color yellowgreen a'''2  \tweak color blue   c'''4
    >>
  }
  {
    <<
      \tweak color mediumvioletred e,4    \tweak color orange g,,2
      \tweak color mediumvioletred e'4    \tweak color orange g2
      \tweak color mediumvioletred e'''4  \tweak color orange g''2
    >>
  }
  {
    <<
      \tweak color mediumvioletred e2     \tweak color orange g,4
      \tweak color mediumvioletred e''2   \tweak color orange g'4
      \tweak color mediumvioletred e''''2 \tweak color orange g'''4
    >>
  }
  {
    <<
      {
        <<
          \tweak color purple d,2   \tweak color red f,,4
          \tweak color purple d'2   \tweak color red f4
          \tweak color purple d'''2 \tweak color red f''4
        >>
      }\\{

        <<
          \tweak color darkturquoise b,4  \tweak color purple d,2
          \tweak color darkturquoise b'4  \tweak color purple d'2
          \tweak color darkturquoise b'''4  \tweak color purple d'''2
        >>
      }
    >>
  }
  {
    <<
      {
        <<
          \tweak color purple d4    \tweak color red f,2
          \tweak color purple d''4  \tweak color red f'2
          \tweak color purple d''''4  \tweak color red f'''2
        >>
      }\\{

        <<
          \tweak color darkturquoise b2   \tweak color purple d4
          \tweak color darkturquoise b''2 \tweak color purple d''4
          \tweak color darkturquoise b''''2 \tweak color purple d''''4
        >>
      }
    >>
  }
}

major-thirds = {
  \clef G
  \key c \major
  {
    <<
      {
        <<
          \tweak color blue   c2     \tweak color mediumvioletred e2
          \tweak color blue   c''2   \tweak color mediumvioletred e''2
          \tweak color blue   c''''2 \tweak color mediumvioletred e''''2
        >>
      }\\{

        <<
          \tweak color blue   c'4    \tweak color mediumvioletred e'4
          \tweak color blue   c'''4  \tweak color mediumvioletred e'''4
        >>
      }
    >>
  }
  {
    <<
      {
        <<
          \tweak color orange g2     \tweak color darkturquoise b2
          \tweak color orange g''2     \tweak color darkturquoise b''2
        >>
      }\\{

        <<
          \tweak color orange g,4     \tweak color darkturquoise b,4
          \tweak color orange g'4     \tweak color darkturquoise b'4
          \tweak color orange g'''4     \tweak color darkturquoise b'''4
        >>
      }
    >>
  }
  {
    <<
      {
        <<
          \tweak color red f,2    \tweak color yellowgreen a,2
          \tweak color red f'2    \tweak color yellowgreen a'2
          \tweak color red f'''2    \tweak color yellowgreen a'''2
        >>
      }\\{

        <<
          \tweak color red f4    \tweak color yellowgreen a4
          \tweak color red f''4    \tweak color yellowgreen a''4
        >>
      }
    >>
  }
}

minor-sixths = {
  \clef G
  \key c \major
  {
    <<
      \tweak color blue   c,4  \tweak color mediumvioletred e,,2
      \tweak color blue   c'4  \tweak color mediumvioletred e2
      \tweak color blue   c'''4  \tweak color mediumvioletred e''2
    >>
  }
  {
    <<
      \tweak color blue   c2  \tweak color mediumvioletred e,4
      \tweak color blue   c''2  \tweak color mediumvioletred e'4
      \tweak color blue   c''''2  \tweak color mediumvioletred e'''4
    >>
  }
  {
    <<
      \tweak color darkturquoise b,,2    \tweak color orange g,4
      \tweak color darkturquoise b2    \tweak color orange g'4
      \tweak color darkturquoise b''2    \tweak color orange g'''4
    >>
  }
  {
    <<
      \tweak color darkturquoise b,,,4    \tweak color orange g,,2
      \tweak color darkturquoise b,4    \tweak color orange g2
      \tweak color darkturquoise b'4    \tweak color orange g''2
      \tweak color darkturquoise b'''4    \tweak color orange g''''2
    >>
  }
  {
    <<
      \tweak color yellowgreen a,2    \tweak color red f4
      \tweak color yellowgreen a'2    \tweak color red f''4
      \tweak color yellowgreen a'''2    \tweak color red f''''4
    >>
  }
  {
    <<
      \tweak color yellowgreen a,,4    \tweak color red f,2
      \tweak color yellowgreen a4    \tweak color red f'2
      \tweak color yellowgreen a''4    \tweak color red f'''2
    >>
  }

}

\score
{
  \header
  {
    piece = "♭3, m3, minor third, liten ters"
  }
  #(genc minor-thirds)
}
\noPageBreak
\score
{
  #(genflats minor-thirds)
}
\noPageBreak
\score
{
  #(gensharps minor-thirds)
}
\noPageBreak
\score
{
  \header
  {
    piece = "6, M6, major sixth, stor sext"
  }
  #(genc major-sixths)
}
\noPageBreak
\score
{
  #(genflats major-sixths)
}
\noPageBreak
\score
{
  #(gensharps major-sixths)
}
\pageBreak

\score
{
  \header
  {
    piece = "3, M3, major third, stor ters"
  }
  #(genc major-thirds)
}
\noPageBreak
\score
{
  #(genflats major-thirds)
}
\noPageBreak
\score
{
  #(gensharps major-thirds)
}
\noPageBreak
\score
{
  \header
  {
    piece = "♭6, m6, minor sixth, liten sext"
  }
  #(genc minor-sixths)
}
\noPageBreak
\score
{
  #(genflats minor-sixths)
}
\noPageBreak
\score
{
  #(gensharps minor-sixths)
}
\pageBreak
%fourths
augmented-fourths = {
  \clef G
  \key c \major
  <<
    \tweak color red f,,4    \tweak color darkturquoise b,,2
    \tweak color red f4    \tweak color darkturquoise b2
    \tweak color red f''4  \tweak color darkturquoise b''2
    \tweak color red f''''4  \tweak color darkturquoise b''''2
  >>
  <<
    \tweak color red f,2   \tweak color darkturquoise b,4
    \tweak color red f'2   \tweak color darkturquoise b'4
    \tweak color red f'''2 \tweak color darkturquoise b'''4
  >>
}

%fifths
diminished-fifths = {
  \clef G
  \key c \major
  <<
    \tweak color darkturquoise b,4    \tweak color red f4
    \tweak color darkturquoise b'4    \tweak color red f''4
    \tweak color darkturquoise b'''4  \tweak color red f''''4
  >>
  <<
    \tweak color darkturquoise b,,2     \tweak color red f,2
    \tweak color darkturquoise b2     \tweak color red f'2
    \tweak color darkturquoise b''2   \tweak color red f'''2
  >>
}


\score
{
  \header
  {
    piece = "aug 4, augmented fourth, överstigande kvart"
  }
  #(genc augmented-fourths)
}
\noPageBreak
\score
{
  #(genflats augmented-fourths)
}
\noPageBreak
\score
{
  #(gensharps augmented-fourths)
}
\noPageBreak
\score
{
  \header
  {
    piece = "dim 5, diminished fifth, förminskad kvint"
  }
  #(genc diminished-fifths)
}
\noPageBreak
\score
{
  #(genflats diminished-fifths)
}
\noPageBreak
\score
{
  #(gensharps diminished-fifths)
}

